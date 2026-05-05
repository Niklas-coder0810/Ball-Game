import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Forest Runner", layout="wide")

st.title("🌍 Forest Runner – Wood UI Edition")

game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>

<style>
body {
    margin: 0;
    overflow: hidden;
    font-family: Arial;

    /* 🪵 Holz Hintergrund außerhalb des Spiels */
    background: linear-gradient(135deg, #c89b63, #e3c08a);
}

/* ---------------- CANVAS ---------------- */
canvas {
    display: block;
    margin: auto;
    border-radius: 12px;

    box-shadow:
        0 20px 50px rgba(0,0,0,0.35),
        inset 0 0 0 6px #8b5a2b;
}

/* ---------------- START SCREEN ---------------- */
#startScreen {
    position: absolute;
    width: 900px;
    height: 420px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(#0b1020, #05060c);
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 10;
    border-radius: 12px;
}

#startScreen h1 {
    font-size: 60px;
}

#startBtn {
    padding: 14px 30px;
    font-size: 20px;
    border: none;
    border-radius: 12px;
    background: #ffd54a;
    cursor: pointer;
}

/* ---------------- SCORE ---------------- */
#score {
    position: absolute;
    top: 10px;
    left: 20px;
    font-size: 20px;
    color: white;

    background: rgba(139, 90, 43, 0.6);
    padding: 6px 12px;
    border-radius: 8px;
}

/* ---------------- GAME OVER ---------------- */
#gameover {
    position: absolute;
    top: 35%;
    width: 100%;
    text-align: center;
    font-size: 60px;
    color: white;
    display: none;
}

/* ---------------- RESTART ---------------- */
#restart {
    position: absolute;
    top: 52%;
    left: 50%;
    transform: translateX(-50%);
    padding: 15px 30px;
    font-size: 20px;
    display: none;
    border-radius: 12px;
    border: none;
    cursor: pointer;
    background: #ffd54a;
}

/* ---------------- UI (BUTTON POSITION FIX) ---------------- */
#ui {
    position: absolute;
    top: 460px;
    left: 50%;
    transform: translateX(-50%);
    width: 900px;
    text-align: center;
}

/* 🪵 Holz Button Style */
button {
    padding: 14px 28px;
    font-size: 18px;
    border: none;
    border-radius: 14px;

    background: linear-gradient(#b07a3a, #8b5a2b);
    color: white;
    cursor: pointer;

    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
}

button:active {
    transform: scale(0.96);
}
</style>
</head>

<body>

<!-- START SCREEN -->
<div id="startScreen">
    <h1>Hallo! 👋</h1>
    <button id="startBtn">START</button>
</div>

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

// ---------------- STATE ----------------
let started = false;
let gameOver = false;

// Start Button
document.getElementById("startBtn").onclick = () => {
    started = true;
    document.getElementById("startScreen").style.display = "none";
};

// ---------------- PLAYER ----------------
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

let score = 0;
let speed = 6;
let time = 0;

// ---------------- INPUT ----------------
function jump() {
    if (!started || gameOver) return;
    if (player.y >= ground) player.vy = -15;
}

document.getElementById("jumpBtn").addEventListener("mousedown", jump);
document.addEventListener("keydown", e => {
    if (e.code === "Space") jump();
});

// ---------------- SPAWN ----------------
setInterval(() => {
    if (started && !gameOver) {
        obstacles.push({ x:900, y:320, w:40, h:40 });
    }
}, 1700);

setInterval(() => {
    if (started && !gameOver) {
        clouds.push({
            x:900,
            y:Math.random()*120+20,
            s:30+Math.random()*30
        });
    }
}, 4000);

// ---------------- PHASE ----------------
function getPhase() {
    let t = time % 60;
    if (t < 20) return 0;
    if (t < 30) return 1;
    if (t < 50) return 2;
    return 3;
}

// ---------------- SKY ----------------
function drawSky(p) {
    let g = ctx.createLinearGradient(0,0,0,420);

    if (p===0){ g.addColorStop(0,"#02030a"); g.addColorStop(1,"#050817"); }
    if (p===1){ g.addColorStop(0,"#1b2a4a"); g.addColorStop(1,"#ff9a6a"); }
    if (p===2){ g.addColorStop(0,"#87ceeb"); g.addColorStop(1,"#e0f6ff"); }
    if (p===3){ g.addColorStop(0,"#ffb36b"); g.addColorStop(1,"#1b1e3a"); }

    ctx.fillStyle = g;
    ctx.fillRect(0,0,900,420);
}

// ---------------- SUN / MOON ----------------
function drawSunMoon(p) {
    ctx.beginPath();

    if (p===2||p===1){
        ctx.fillStyle="#ffd84d";
        ctx.arc(750,80,35,0,Math.PI*2);
    } else {
        ctx.fillStyle="#dcdcdc";
        ctx.arc(750,80,30,0,Math.PI*2);
    }

    ctx.fill();
}

// ---------------- STARS ----------------
function drawStars(p) {
    if (p!==0) return;
    ctx.fillStyle="white";
    for(let i=0;i<60;i++){
        ctx.fillRect(Math.random()*900,Math.random()*200,2,2);
    }
}

// ---------------- TREES ----------------
function drawTrees(p) {
    for(let i=0;i<18;i++){
        let x=i*60;
        ctx.fillStyle = (p===0) ? "#05070c" : "#1f3b2a";
        ctx.fillRect(x,260,20,160);
        ctx.beginPath();
        ctx.arc(x+10,260,30,0,Math.PI*2);
        ctx.fill();
    }
}

// ---------------- GROUND ----------------
function drawGround(){
    ctx.fillStyle="#1a1f2e";
    ctx.fillRect(0,340,900,80);
}

// ---------------- CLOUDS ----------------
function drawClouds(){
    ctx.fillStyle="rgba(255,255,255,0.7)";
    for(let c of clouds){
        ctx.beginPath();
        ctx.arc(c.x,c.y,c.s,0,Math.PI*2);
        ctx.fill();
        c.x-=1.2;
    }
    clouds = clouds.filter(c=>c.x>-100);
}

// ---------------- UPDATE ----------------
function update(){
    if(!started||gameOver) return;

    time+=0.02;

    player.y+=player.vy;
    if(player.y<ground) player.vy+=gravity;
    else { player.y=ground; player.vy=0; }

    for(let o of obstacles) o.x-=speed;

    score++;
    document.getElementById("score").innerText =
        "Score: "+Math.floor(score/10);

    if(score%200===0) speed+=0.5;

    for(let o of obstacles){
        if(
            player.x<o.x+o.w &&
            player.x+player.w>o.x &&
            player.y<o.y+o.h &&
            player.y+player.h>o.y
        ){
            endGame();
        }
    }

    obstacles = obstacles.filter(o=>o.x>-100);
}

// ---------------- DRAW ----------------
function drawPlayer(){
    ctx.fillStyle="#ffd54a";
    ctx.fillRect(player.x,player.y,player.w,player.h);

    ctx.fillStyle="black";
    ctx.fillRect(player.x+6,player.y+8,3,3);
    ctx.fillRect(player.x+16,player.y+8,3,3);
}

function drawObstacles(){
    ctx.fillStyle="#7a4a1f";
    for(let o of obstacles) ctx.fillRect(o.x,o.y,o.w,o.h);
}

// ---------------- GAME OVER ----------------
function endGame(){
    gameOver=true;
    document.getElementById("gameover").style.display="block";
    document.getElementById("restart").style.display="block";
}

function resetGame(){
    started=false;
    gameOver=false;
    score=0;
    speed=6;
    obstacles=[];
    clouds=[];
    player.y=ground;
    player.vy=0;

    document.getElementById("gameover").style.display="none";
    document.getElementById("restart").style.display="none";
    document.getElementById("startScreen").style.display="flex";
}

// ---------------- LOOP ----------------
function loop(){
    let p=getPhase();

    drawSky(p);
    drawStars(p);
    drawSunMoon(p);
    drawTrees(p);
    drawClouds();
    drawGround();

    update();
    drawPlayer();
    drawObstacles();

    requestAnimationFrame(loop);
}

loop();
</script>

</body>
</html>
"""

components.html(game_html, height=700)
