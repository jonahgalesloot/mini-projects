const {
    ipcRenderer
} = require('electron');

document.addEventListener('keydown', (event) => {
    if (event.key === 'f') {
        ipcRenderer.send('enter-fullscreen');
    }
    if (event.key === 'Escape') {
        ipcRenderer.send('exit-fullscreen');
    }
});

ipcRenderer.on('fullscreen-changed', (event, isFullScreen) => {
    if (isFullScreen) {
        showPopup();
    }
});

function showPopup() {
    const popup = document.createElement('div');
    popup.textContent = 'Press ESC to return';
    popup.style.position = 'fixed';
    popup.style.top = '20px';
    popup.style.right = '20px';
    popup.style.padding = '10px';
    popup.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
    popup.style.color = 'white';
    popup.style.borderRadius = '5px';
    popup.style.transition = 'opacity 0.5s';
    document.body.appendChild(popup);

    setTimeout(() => {
        popup.style.opacity = '0';
        setTimeout(() => popup.remove(), 500);
    }, 3000);
}
let scheduledChargeShot = null;
let projectiles = [];
let explosions = [];
let baseShipDimensions;
let canvas, ctx;
let lastFrameTime = performance.now();
const cappedFPS = 30;
const frameDuration = 1000 / cappedFPS;
let keysPressed = {
    a: false,
    d: false,
    space: false
};
const explosion_frameDelay = 100;

const SHOW_HITBOXES = false;

const playerAttributes = {
    speed: 720,
    width: 72,
    height: 72,
    x: 0,

    animations: {
        idle: [],
        turn_left: [],
        turn_right: [],
        shoot: [],
        charge: [],
        damage: [],
        death: []
    },

    animationLengths: {
        idle: 1,
        turn_left: 3,
        turn_right: 3,
        shoot: 2,
        charge: 4,
        damage: 5,
        death: 15
    },

    animationPriorities: {
        idle: 1,
        turn_left: 2,
        turn_right: 2,
        shoot: 3,
        charge: 4,
        damage: 5,
        death: 6
    },
    animationState: "idle",
    currentFrame: 0,
    frameDelay: 100,
    minCharge: 0.35,
    lastFrameTime: 0,
    shotCooldown: 0.1,
    shotTimeSince: 0,
    chargeTime: 0,
    processedAnimations: {},
    isAnimationComplete: false,
    isTurning: false,
    overloadCD: 1,
    overloaded: 0
};

const charging = {
    max: 3,
    overload: 6
};

const projectileAnimations = {
    quickCharge: [],
    quickExplode: [],
    chargedCharge: [],
    chargedExplode: [],
    overload: [],
    invis: []
};

const explosionSounds = {
    quick: new Audio("Sounds/explosion_quick.mp3"),
    charged: new Audio("Sounds/explosion_charged.mp3"),
    overload: new Audio("Sounds/explosion_overload.mp3")
};

function startGame() {
    document.getElementById("startScreen").style.display = "none";
    document.getElementById("gameScreen").style.display = "flex";
    playerAttributes.x = (canvas.width - playerAttributes.width) / 2;
    console.log("Game started. Initial state: idle");
    requestAnimationFrame(frameUpdate);
}

function frameUpdate(currentTime) {
    let deltaTime = (currentTime - lastFrameTime) / 1000;
    if (currentTime - lastFrameTime >= frameDuration) {
        lastFrameTime = currentTime;
        updatePlayer(deltaTime);
        updateAnimation(deltaTime);
        drawGame();
    }
    requestAnimationFrame(frameUpdate);
    updateValues()
}

function updateValues() {
    screen = document.getElementById("gameScreen");
    playerAttributes.speed = screen.width / 2;
    playerAttributes.width = screen.width / 10;
    playerAttributes.height = screen.width / 10;

}

function updateAnimation(deltaTime) {
    if (playerAttributes.animationState !== "idle") {
        playerAttributes.currentFrame += deltaTime * 1000 / playerAttributes.frameDelay;
        if (playerAttributes.currentFrame >= playerAttributes.animationLengths[playerAttributes.animationState]) {
            console.log(`Animation '${playerAttributes.animationState}' completed.`);
            if (playerAttributes.animationState === "death") {
                console.log("Death animation completed. Restarting game.");
                document.getElementById("gameScreen").style.display = "none";
                document.getElementById("startScreen").style.display = "flex";
            } else if ((playerAttributes.animationState === "turn_left" && keysPressed.a) ||
                (playerAttributes.animationState === "turn_right" && keysPressed.d)) {

                playerAttributes.currentFrame = playerAttributes.animationLengths[playerAttributes.animationState] - 1;
                playerAttributes.isTurning = true;
            } else {
                setPlayerState("idle");
                playerAttributes.currentFrame = 0;
                playerAttributes.lastFrameTime = performance.now();
                playerAttributes.isTurning = false;
            }
            playerAttributes.isAnimationComplete = true;
        }
    }
}

class Projectile {
    constructor(x, y, type, chargeTime = 0) {
        this.x = x;
        this.y = y;
        this.type = type;
        this.explosionCreated = false;
        this.done = false;

        const clampedChargeTime = Math.min(chargeTime, charging.max);

        if (type === "quick") {
            this.targetHeight = canvas.height * 0.25;
            this.damage = 5;
            this.speed = 1000;
            this.radius = 50;
            this.width = 3;
            this.height = 12;
        } else if (type === "charged") {

            let chargeMs = clampedChargeTime * 1000;

            this.radius = 20 + Math.sqrt(clampedChargeTime) * 150;

            let air_time = Math.max(
                2 * ((1.6 / -1.692e7) * (chargeMs - 180) * (chargeMs - 5020)),
                0.3
            );

            if (chargeTime >= charging.max) this.speed = 400;
            else this.speed = Math.max(1200 / (1 + 0.001 * chargeMs), 150);
            this.targetHeight = Math.max(this.y - this.speed * air_time, 0);

            this.damage = (5 + clampedChargeTime * 5);

            this.width = 6;
            this.height = 56;
        } else if (type === "overload") {
            this.damage = 50;
            this.speed = 10;
            this.targetHeight = this.y + 5;
            this.radius = 800;
            this.width = 30;
            this.height = 30;
        }

        this.damage *= (0.8 + Math.random() * 0.4);
        this.speed *= (0.8 + Math.random() * 0.4);
        this.targetHeight *= (0.8 + Math.random() * 0.4);
        this.radius *= (0.8 + Math.random() * 0.4);

        if (type !== "overload") this.img = projectileAnimations[type + "Charge"];
        else this.img = projectileAnimations["invis"];
    }

    update(deltaTime) {
        if (this.done) return false;

        if (this.type === "overload" && !this.explosionCreated) {
            explosions.push(new Explosion(this.x, this.y, this.radius, this.damage, this.type));
            explosionSounds.overload.currentTime = 0;
            explosionSounds.overload.play();
            this.explosionCreated = true;
            this.done = true;
            return false;
        }

        this.y -= this.speed * deltaTime;

        if (this.y <= this.targetHeight && !this.explosionCreated) {
            explosions.push(new Explosion(this.x, this.y, this.radius, this.damage, this.type));

            if (this.type === "quick") {
                explosionSounds.quick.currentTime = 0;
                explosionSounds.quick.play();
            } else if (this.type === "charged") {
                explosionSounds.charged.currentTime = 0;
                explosionSounds.charged.play();
            }

            this.explosionCreated = true;
            this.done = true;
        }

        if (this.y < 0) {
            this.done = true;
            return false;
        }

        return true;
    }

    draw(ctx) {
        if (this.img) {
            ctx.drawImage(
                this.img,
                this.x - this.width / 2,
                this.y - this.height / 2,
                this.width,
                this.height
            );
        } else {

            ctx.fillStyle = this.type === "quick" ? "blue" : "red";
            ctx.fillRect(this.x - this.width / 2, this.y - this.height / 2, this.width, this.height);
        }

        if (SHOW_HITBOXES) {
            ctx.strokeStyle = "purple";
            ctx.lineWidth = 2;
            ctx.strokeRect(
                this.x - this.width / 2,
                this.y - this.height / 2,
                this.width,
                this.height
            );
        }
    }
}

class Explosion {
    constructor(x, y, radius, damage, type) {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.damage = damage;
        this.frames = [];

        if (type === "quick") this.frames = projectileAnimations.quickExplode;
        if (type === "charged") this.frames = projectileAnimations.chargedExplode;
        if (type === "overload") this.frames = projectileAnimations.overload;

        this.totalFrames = this.frames.length;
        this.frameDuration = explosion_frameDelay / 1000;
        this.duration = this.totalFrames * this.frameDuration;
        this.timer = 0;
        this.done = false;
        this.opacity = 1;
        this.currentFrame = 0;
        this.img = this.frames[0];

        console.log("Explosion created at", this.x, this.y, "with radius", this.radius, "damage", this.damage, "duration", this.duration);
    }

    update(deltaTime) {
        if (this.done) return false;

        this.timer += deltaTime;

        this.currentFrame = Math.min(Math.floor(this.timer / this.frameDuration), this.totalFrames - 1);
        this.img = this.frames[this.currentFrame];

        let shrinkFactor = 0.90;
        this.radius *= shrinkFactor;
        this.opacity *= 0.95;

        if (this.timer >= this.duration) {
            this.done = true;
        }

        return true;
    }

    draw(ctx) {
        if (this.done) return;

        ctx.save();
        ctx.globalAlpha = this.opacity;

        if (this.img) {
            ctx.drawImage(
                this.img,
                this.x - this.radius,
                this.y - this.radius,
                this.radius * 2,
                this.radius * 2
            );
        }

        ctx.restore();

        if (SHOW_HITBOXES) {
            ctx.strokeStyle = "yellow";
            ctx.lineWidth = 2;
            ctx.strokeRect(this.x - this.radius, this.y - this.radius, this.radius * 2, this.radius * 2);
        }
    }
}

function updatePlayer(deltaTime) {
    let moving = false;
    let speedMultiplier = 1;

    playerAttributes.shotTimeSince += deltaTime;
    if (playerAttributes.chargeTime >= playerAttributes.minCharge) {
        speedMultiplier = 0.66;
    }
    if (playerAttributes.chargeTime >= charging.max) {
        speedMultiplier = 0.33;
    }
    if (playerAttributes.overloaded > 0) {
        playerAttributes.overloaded -= deltaTime;
        speedMultiplier = 0;
    }
    if (keysPressed.a && playerAttributes.x > 0) {
        playerAttributes.x -= playerAttributes.speed * deltaTime * speedMultiplier;
        setPlayerState("turn_left");
        moving = true;
    }
    if (keysPressed.d && playerAttributes.x < canvas.width - playerAttributes.width) {
        playerAttributes.x += playerAttributes.speed * deltaTime * speedMultiplier;
        setPlayerState("turn_right");
        moving = true;
    }
    if (keysPressed.space && playerAttributes.overloaded <= 0) {
        playerAttributes.chargeTime += deltaTime;
        if (playerAttributes.chargeTime > charging.overload) {
            damagePlayer();
            projectiles.push(new Projectile(
                playerAttributes.x + playerAttributes.width / 2,
                canvas.height - playerAttributes.height,
                "overload"
            ));
            playerAttributes.overloaded = playerAttributes.overloadCD
            playerAttributes.chargeTime = 0;
        }
    } else {
        if (playerAttributes.chargeTime > playerAttributes.minCharge) {
            setPlayerState("charge");
            let chargeY = canvas.height - playerAttributes.height;
            let chargeTime = playerAttributes.chargeTime;

            scheduledChargeShot = setTimeout(() => {
                projectiles.push(new Projectile((playerAttributes.x + playerAttributes.width / 2), chargeY, "charged", chargeTime));
            }, playerAttributes.frameDelay * (playerAttributes.animationLengths["charge"] - 1));

        } else if (playerAttributes.chargeTime > 0 && playerAttributes.shotTimeSince > playerAttributes.shotCooldown) {
            setPlayerState("shoot");
            projectiles.push(new Projectile(
                playerAttributes.x + playerAttributes.width / 2,
                canvas.height - playerAttributes.height,
                "quick"

            ));
            playerAttributes.shotTimeSince = 0;
        }
        playerAttributes.chargeTime = 0;

    }

    if (!moving && !keysPressed.space) {
        setPlayerState("idle");
    }
}

function damagePlayer() {
    setPlayerState("damage");
}

function frameUpdate(currentTime) {
    let deltaTime = (currentTime - lastFrameTime) / 1000;
    if (currentTime - lastFrameTime >= frameDuration) {
        lastFrameTime = currentTime;
        updatePlayer(deltaTime);
        updateAnimation(deltaTime);
        projectiles = projectiles.filter(p => p.update(deltaTime));
        explosions = explosions.filter(e => e.update(deltaTime))
        drawGame();
    }
    requestAnimationFrame(frameUpdate);
}

function drawGame() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawPlayer(ctx);

    if (playerAttributes.chargeTime >= charging.max) {
        drawMaxChargeEffects(ctx);
    }

    if (playerAttributes.chargeTime > playerAttributes.minCharge) {
        let centerX = playerAttributes.x + playerAttributes.width / 2;
        let centerY = canvas.height - playerAttributes.height / 2 - 10;

        ctx.save();

        const minFrequency = 0.5;
        const maxFrequency = 4;
        const frequency = minFrequency + (charging.overload - 1) * (maxFrequency - minFrequency) / 5;

        ctx.globalAlpha = 0.5 + Math.sin(performance.now() * 0.001 * frequency) * 0.3;

        ctx.fillStyle = "rgba(255, 255, 255, 0.4)";
        ctx.beginPath();
        ctx.arc(centerX, centerY, 50, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }

    for (let p of projectiles) {
        p.draw(ctx);
    }

    for (let e of explosions) {
        e.draw(ctx);
    }
}

function drawPlayer(ctx) {
    let frames = playerAttributes.processedAnimations[playerAttributes.animationState];

    if (!frames || frames.length === 0) return;

    let frameIndex;
    if (playerAttributes.animationState === "idle" ||
        (playerAttributes.isAnimationComplete && !playerAttributes.isTurning)) {
        frameIndex = 0;
    } else {
        frameIndex = Math.min(Math.floor(playerAttributes.currentFrame), frames.length - 1);
    }

    let currentImage;
    if (playerAttributes.chargeTime > playerAttributes.minCharge &&
        playerAttributes.animationPriorities[playerAttributes.animationState] <= 3) {
        currentImage = playerAttributes.processedAnimations["charge"][2];
    } else {
        currentImage = frames[frameIndex];
    }

    let xOffset = (currentImage.width - playerAttributes.width) / 2;
    let yOffset = (currentImage.height - playerAttributes.height) / 2;

    let shakeAmount = (playerAttributes.chargeTime >= charging.max) ? (Math.random() - 0.5) * 5 : 0;
    let drawX = playerAttributes.x - xOffset + shakeAmount;
    let drawY = canvas.height - playerAttributes.height - 10 - yOffset + shakeAmount;

    ctx.save();
    ctx.filter = 'brightness(0) saturate(100%)';
    for (let dx = -1; dx <= 1; dx++) {
        for (let dy = -1; dy <= 1; dy++) {
            if (dx !== 0 || dy !== 0) {
                ctx.drawImage(currentImage, drawX + dx, drawY + dy, currentImage.width, currentImage.height);
            }
        }
    }
    ctx.restore();

    ctx.save();
    ctx.globalCompositeOperation = 'source-atop';
    ctx.fillStyle = 'white';
    ctx.fillRect(drawX, drawY, currentImage.width, currentImage.height);
    ctx.restore();

    ctx.drawImage(currentImage, drawX, drawY, currentImage.width, currentImage.height);

    if (SHOW_HITBOXES) {
        ctx.strokeStyle = 'red';
        ctx.lineWidth = 2;
        ctx.strokeRect(playerAttributes.x, canvas.height - playerAttributes.height - 10,
            playerAttributes.width, playerAttributes.height);
    }
}

function drawMaxChargeEffects(ctx) {
    let centerX = playerAttributes.x + playerAttributes.width / 2;
    let centerY = canvas.height - playerAttributes.height / 2 - 10;

    ctx.save();

    ctx.filter = 'brightness(200%)';
    ctx.beginPath();

    for (let i = 0; i < 20; i++) {
        ctx.strokeStyle = "white";
        ctx.lineWidth = 2;
        ctx.beginPath();
        let x1 = centerX + (Math.random() - 0.5) * 30;
        let y1 = centerY + (Math.random() - 0.5) * 30;
        let x2 = x1 + (Math.random() - 0.5) * 10;
        let y2 = y1 + (Math.random() - 0.5) * 10;
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.stroke();
    }
    ctx.filter = 'none';
    ctx.restore();
}

function setPlayerState(newState) {
    if ((playerAttributes.animationPriorities[newState] > playerAttributes.animationPriorities[playerAttributes.animationState] ||
            playerAttributes.animationState === "idle" ||
            playerAttributes.isAnimationComplete) && playerAttributes.animationState !== newState && playerAttributes.isTurning === false) {
        console.log(`Changing animation from '${playerAttributes.animationState}' to '${newState}'`);
        playerAttributes.animationState = newState;
        playerAttributes.currentFrame = 0;
        playerAttributes.lastFrameTime = performance.now();
        playerAttributes.isAnimationComplete = false;
        playerAttributes.isTurning = false;
    }
}

function processPlayerSprite(image) {
    const tempCanvas = document.createElement('canvas');
    const tempCtx = tempCanvas.getContext('2d');
    const trimmedImage = trimTransparentPixels(image);

    tempCanvas.width = trimmedImage.height;
    tempCanvas.height = trimmedImage.width;
    tempCtx.translate(tempCanvas.width / 2, tempCanvas.height / 2);
    tempCtx.rotate(-Math.PI / 2);
    tempCtx.drawImage(trimmedImage, -trimmedImage.width / 2, -trimmedImage.height / 2);

    const scaledCanvas = document.createElement('canvas');
    const scaledCtx = scaledCanvas.getContext('2d');
    scaledCanvas.width = playerAttributes.width;
    scaledCanvas.height = playerAttributes.height;
    scaledCtx.drawImage(tempCanvas, 0, 0, tempCanvas.width, tempCanvas.height,
        0, 0, playerAttributes.width, playerAttributes.height);
    return scaledCanvas;
}

function trimTransparentPixels(image) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = image.width;
    canvas.height = image.height;
    ctx.drawImage(image, 0, 0);
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const {
        data,
        width,
        height
    } = imageData;
    let minX = width,
        minY = height,
        maxX = 0,
        maxY = 0;
    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            const alpha = data[(y * width + x) * 4 + 3];
            if (alpha !== 0) {
                minX = Math.min(minX, x);
                minY = Math.min(minY, y);
                maxX = Math.max(maxX, x);
                maxY = Math.max(maxY, y);
            }
        }
    }
    const trimmedCanvas = document.createElement('canvas');
    const trimmedCtx = trimmedCanvas.getContext('2d');
    let trimmedWidth = maxX - minX + 1;
    let trimmedHeight = maxY - minY + 1;

    if (baseShipDimensions != null) {
        trimmedWidth = Math.max(trimmedWidth, baseShipDimensions.width);
        trimmedHeight = Math.max(trimmedHeight, baseShipDimensions.height);
    }

    trimmedCanvas.width = trimmedWidth;
    trimmedCanvas.height = trimmedHeight;

    const offsetX = (trimmedWidth - (maxX - minX + 1)) / 2;
    const offsetY = (trimmedHeight - (maxY - minY + 1)) / 2;

    trimmedCtx.drawImage(image, minX, minY, maxX - minX + 1, maxY - minY + 1,
        offsetX, offsetY, maxX - minX + 1, maxY - minY + 1);

    return trimmedCanvas;
}

function preloadPlayerAnimations() {
    let imagesLoaded = 0;
    const totalImages = Object.keys(playerAttributes.animations).reduce((sum, type) => sum + playerAttributes.animationLengths[type], 0);

    Object.keys(playerAttributes.animations).forEach(type => {
        playerAttributes.processedAnimations[type] = new Array(playerAttributes.animationLengths[type]);

        for (let i = 0; i < playerAttributes.animationLengths[type]; i++) {
            let img = new Image();
            img.src = i <= 9 ?
                `Sprites/Player/${type}/tile00${i}.png` :
                `Sprites/Player/${type}/tile0${i}.png`;

            img.onload = () => {
                let processedImg = processPlayerSprite(img);
                playerAttributes.processedAnimations[type][i] = processedImg;

                imagesLoaded++;
                console.log(`Loaded frame ${i} for ${type}`);

                if (imagesLoaded === totalImages) {
                    console.log("All images preloaded!");
                }

                if (type === "idle" && i === 0) {
                    initializeBaseShipDimensions(img);
                }
            };

            img.onerror = () => {
                console.error("Error loading image:", img.src);
            };
        }
    });
}

function initializeBaseShipDimensions(idleSprite) {
    const trimmedIdle = trimTransparentPixels(idleSprite);
    baseShipDimensions = {
        width: trimmedIdle.width,
        height: trimmedIdle.height
    };
}

function trimFullyTransparentPixels(image) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = image.width;
    canvas.height = image.height;
    ctx.drawImage(image, 0, 0);
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const {
        data,
        width,
        height
    } = imageData;
    let minX = width,
        minY = height,
        maxX = 0,
        maxY = 0;
    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            const alpha = data[(y * width + x) * 4 + 3];
            if (alpha !== 0) {
                minX = Math.min(minX, x);
                minY = Math.min(minY, y);
                maxX = Math.max(maxX, x);
                maxY = Math.max(maxY, y);
            }
        }
    }
    const trimmedCanvas = document.createElement('canvas');
    const trimmedCtx = trimmedCanvas.getContext('2d');
    trimmedCanvas.width = maxX - minX + 1;
    trimmedCanvas.height = maxY - minY + 1;
    trimmedCtx.drawImage(image, minX, minY, maxX - minX + 1, maxY - minY + 1, 0, 0, maxX - minX + 1, maxY - minY + 1);
    return trimmedCanvas;
}

function preloadProjectileAnimations() {
    const types = ["quickExplode", "chargedExplode"];
    const chargeTypes = ["quickCharge", "chargedCharge"];

    let imagesLoaded = 0;
    let totalImages = types.reduce((sum, type) => sum + 5, 0);
    totalImages += chargeTypes.length;

    types.forEach(type => {
        projectileAnimations[type] = [];
        if (type === "quickExplode") frameCount = 8;
        else frameCount = 9;
        for (let i = 0; i < frameCount; i++) {
            let img = new Image();
            img.src = `Sprites/Projectiles/${type}/tile00${i}.png`;

            img.onload = () => {
                let processedImg = trimFullyTransparentPixels(img);
                projectileAnimations[type].push(processedImg);
                imagesLoaded++;
                console.log(`Loaded projectile frame ${i} for ${type}`);

            };
            img.onerror = () => {
                console.error("Error loading projectile image:", img.src);
            };
        }
    });

    chargeTypes.forEach(type => {
        projectileAnimations[type] = [];
        let img = new Image();
        img.src = `Sprites/Projectiles/${type}.png`;

        img.onload = () => {

            projectileAnimations[type] = img;
            imagesLoaded++;
            console.log(`Loaded projectile image for ${type}`);

        };
        img.onerror = () => {
            console.error("Error loading projectile image:", img.src);
        };
    });

    projectileAnimations["overload"] = []
    for (let i = 0; i < 9; i++) {
        let img = new Image();
        img.src = `Sprites/Projectiles/overload/tile00${i}.png`;

        img.onload = () => {

            projectileAnimations["overload"].push(img);
            imagesLoaded++;
            console.log(`Loaded projectile frame ${i} for overload`);

        };
        img.onerror = () => {
            console.error("Error loading projectile image:", img.src);
        };
    }

    projectileAnimations["invis"] = [];
    let img = new Image();
    img.src = `Sprites/Projectiles/father.png`;

    img.onload = () => {
        let processedImg = trimFullyTransparentPixels(img);
        projectileAnimations["invis"] = processedImg;
        imagesLoaded++;
        console.log(`Loaded projectile image for invis`);

    };
    img.onerror = () => {
        console.error("Error loading projectile image:", img.src);
    };

    if (imagesLoaded === totalImages) {
        console.log("All projectile images preloaded!");
    }
}

document.addEventListener("DOMContentLoaded", function() {
    canvas = document.getElementById("gameCanvas");
    ctx = canvas.getContext("2d");

    function resizeCanvas() {
        canvas.width = document.getElementById("gameContainer").clientWidth;
        canvas.height = document.getElementById("gameContainer").clientHeight;
    }
    resizeCanvas();
    window.addEventListener("resize", resizeCanvas);
    preloadPlayerAnimations();
    preloadProjectileAnimations();

    Object.values(explosionSounds).forEach(sound => {
        sound.volume = 0.8;
        sound.preload = "auto";
    });
    document.getElementById("startButton").addEventListener("click", startGame);
    document.addEventListener("keydown", (e) => {
        if (e.code === "KeyA") {
            keysPressed.a = true;
            keysPressed.d = false;
        }
        if (e.code === "KeyD") {
            keysPressed.d = true;
            keysPressed.a = false;
        }
        if (e.code === "Space") keysPressed.space = true;
        if (e.code == "KeyL") {
            setPlayerState("damage");
        }
        if (e.code == "KeyK") {
            setPlayerState("death");
        }
    });
    document.addEventListener("keyup", (e) => {
        if (e.code === "KeyA") keysPressed.a = false;
        if (e.code === "KeyD") keysPressed.d = false;
        if (e.code === "Space") keysPressed.space = false;
    });
});