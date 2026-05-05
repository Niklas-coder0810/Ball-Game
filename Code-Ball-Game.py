import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Forest Runner", layout="wide")

st.title("🌍 Forest Runner – Day & Night Cycle")

game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>

<style>
    body {
        margin: 0;
        overflow: hidden;
        background: #000;
    }

    canvas {
        display: block;
        margin: auto;
        border-radius: 12px;
    }

    #score {
        position: absolute;
        top: 10px;
        left: 20px;
        font-size: 20px;
        color: white;
        font-family: Arial;
    }

    #gameover {
        position: absolute;
        top: 30%;
        width: 100%;
        text-align: center;
        font-size: 60px;
        color: white;
        display: none;
        font-weight: bold;
    }

    #restart {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translateX(-50%);
        padding: 15px 30px;
        font-size: 20px;
        display: none;
        border-radius: 12px;
        border: none;
        cursor: pointer;
    }

    #ui {
        position: absolute;
        bottom: 20px;
        width: 100%;
        text-align: center;
    }

    button {
        padding: 14px 28px;
        font-size: 18px;
        border: none;
        border-radius: 12px;
        background: #1b2440;
        color: white;
        cursor: pointer;
    }
</style>
</head>

<body>

<canvas id="game" width="900" height="420"></canvas>

<div id="score">Score: 0</div>
<div id="gameover">GAME OVER</div>
<button id="restart" onclick="resetGame()">Neustart</button>

<div id="ui">
    <button id="jumpBtn">⬆ SPRINGEN</button>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let score = 0;
let gameOver = false;
let speed = 6;

let time = 0;

// 🌗 Cycle: 60s total
function getPhase() {
    let t = time % 60;
    if (t < 20) return 0;   // night
    if (t < 30) return 1;   // sunrise
    if (t < 50) return 2;   // day
    return 3;               // sunset
}

let player = {
    x: 120,
    y: 300,
    w: 28,
    h: 28,
    vy: 0
};

let gravity = 1.1;
let ground = 300;

let obstacles = [];
let clouds = [];

// ---------------- INPUT ----------------

function jump() {
    if (player.y >= ground && !gameOver) {
        player.vy = -15;
    }
}

document.getElementById("jumpBtn").addEventListener("mousedown", jump);
document.getElementById("jumpBtn").addEventListener("touchstart", function(e){
    e.preventDefault();
    jump();
});

document.addEventListener("keydown", function(e){
    if (e.code === "Space") jump();
});

// ---------------- SPAWN ----------------

function spawnObstacle() {
    if (gameOver) return;

    obstacles.push({
        x: 900,
        y: 320,
        w: 40,
        h: 40
    });
}

setInterval(spawnObstacle, 1700);

function spawnCloud() {
    clouds.push({
        x: 900,
        y: Math.random() * 120 + 20,
        s: Math.random() * 30 + 30
    });
}
setInterval(spawnCloud, 4000);

// ---------------- DRAW SKY ----------------

function drawSky(phase) {
    let g = ctx.createLinearGradient(0, 0, 0, 420);

    if (phase === 0) { // night
        g.addColorStop(0, "#02030a");
        g.addColorStop(1, "#050817");
    }
    if (phase === 1) { // sunrise
        g.addColorStop(0, "#1b2a4a");
        g.addColorStop(1, "#ff9a6a");
    }
    if (phase === 2) { // day
        g.addColorStop(0, "#87ceeb");
        g.addColorStop(1, "#e0f6ff");
    }
    if (phase === 3) { // sunset
        g.addColorStop(0, "#ffb36b");
        g.addColorStop(1, "#1b1e3a");
    }

    ctx.fillStyle = g;
    ctx.fillRect(0, 0, 900, 420);
}

// ---------------- SUN / MOON ----------------

function drawSunMoon(phase) {
    ctx.beginPath();

    if (phase === 2 || phase === 1) {
        ctx.fillStyle = "#ffd84d"; // sun
        ctx.arc(750, 80, 35, 0, Math.PI * 2);
    } else {
        ctx.fillStyle = "#dcdcdc"; // moon
        ctx.arc(750, 80, 30, 0, Math.PI * 2);
    }

    ctx.fill();
}

// ---------------- STARS ----------------

function drawStars(phase) {
    if (phase !== 0) return;

    ctx.fillStyle = "white";
    for (let i = 0; i < 80; i++) {
        ctx.fillRect(Math.random()*900, Math.random()*220, 2, 2);
    }
}

// ---------------- TREES ----------------

function drawTrees(phase) {
    for (let i = 0; i < 18; i++) {
        let x = i * 60;

        ctx.fillStyle = (phase === 0) ? "#05070c" : "#1f3b2a";

        ctx.fillRect(x, 260, 20, 160);
        ctx.beginPath();
        ctx.arc(x + 10, 260, 30, 0, Math.PI * 2);
        ctx.fill();
    }
}

// ---------------- GROUND ----------------

function drawGround() {
    ctx.fillStyle = "#1a1f2e";
    ctx.fillRect(0, 340, 900, 80);
}

// ---------------- CLOUDS ----------------

function drawClouds() {
    ctx.fillStyle = "rgba(255,255,255,0.7)";

    for (let c of clouds) {
        ctx.beginPath();
        ctx.arc(c.x, c.y, c.s, 0, Math.PI * 2);
        ctx.fill();
        c.x -= 1.2;
    }

    clouds = clouds.filter(c => c.x > -100);
}

// ---------------- UPDATE ----------------

function update() {
    if (gameOver) return;

    time += 0.02;

    player.y += player.vy;

    if (player.y < ground) player.vy += gravity;
    else {
        player.y = ground;
        player.vy = 0;
    }

    for (let o of obstacles) o.x -= speed;

    score++;
    document.getElementById("score").innerText =
        "Score: " + Math.floor(score / 10);

    if (score % 200 === 0) speed += 0.5;

    for (let o of obstacles) {
        if (
            player.x < o.x + o.w &&
            player.x + player.w > o.x &&
            player.y < o.y + o.h &&
            player.y + player.h > o.y
        ) {
            endGame();
        }
    }

    obstacles = obstacles.filter(o => o.x > -100);
}

// ---------------- DRAW ----------------

function drawPlayer() {
    ctx.fillStyle = "#ffd54a";
    ctx.fillRect(player.x, player.y, player.w, player.h);

    ctx.fillStyle = "black";
    ctx.fillRect(player.x + 6, player.y + 8, 3, 3);
    ctx.fillRect(player.x + 16, player.y + 8, 3, 3);
}

function drawObstacles() {
    ctx.fillStyle = "#7a4a1f";

    for (let o of obstacles) {
        ctx.fillRect(o.x, o.y, o.w, o.h);
    }
}

// ---------------- LOOP ----------------

function loop() {
    let phase = getPhase();

    drawSky(phase);
    drawStars(phase);
    drawSunMoon(phase);
    drawTrees(phase);
    drawClouds();
    drawGround();

    update();
    drawPlayer();
    drawObstacles();

    requestAnimationFrame(loop);
}

// ---------------- GAME OVER ----------------

function endGame() {
    gameOver = true;
    document.getElementById("gameover").style.display = "block";
    document.getElementById("restart").style.display = "block";
}

function resetGame() {
    score = 0;
    speed = 6;
    gameOver = false;
    obstacles = [];
    clouds = [];
    player.y = ground;
    player.vy = 0;

    document.getElementById("gameover").style.display = "none";
    document.getElementById("restart").style.display = "none";
}

loop();
</script>

</body>
</html>
"""

components.html(game_html, height=600)
