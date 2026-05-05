import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Runner Game", layout="wide")

st.title("🌍 Runner Game – Forest & Beach Mode")

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
    background: linear-gradient(135deg, #c89b63, #e3c08a);
}

/* ---------------- CANVAS ---------------- */
canvas {
    display: block;
    margin: auto;
    border-radius: 12px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.4),
                inset 0 0 0 6px #8b5a2b;
}

/* ---------------- MENU ---------------- */
#menu {
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

#menu h1 {
    font-size: 50px;
    margin-bottom: 20px;
}

.menuBtn {
    padding: 14px 28px;
    font-size: 18px;
    margin: 10px;
    border-radius: 12px;
    border: none;
    cursor: pointer;
    background: linear-gradient(#b07a3a, #8b5a2b);
    color: white;
}

/* ---------------- UI ---------------- */
#score, #level {
    position: absolute;
    top: 10px;
    color: white;
    padding: 8px 14px;
    border-radius: 10px;
    background: rgba(0,0,0,0.4);
}

#score { left: 20px; }
#level { right: 20px; }

#gameover {
    position: absolute;
    top: 35%;
    width: 100%;
    text-align: center;
    font-size: 60px;
    color: white;
    display: none;
}

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
    background: #ffd54a;
}

/* ---------------- BUTTON ---------------- */
#ui {
    position: absolute;
    top: 460px;
    left: 50%;
    transform: translateX(-50%);
    width: 900px;
    text-align: center;
}

button {
    padding: 16px 32px;
    font-size: 20px;
    border-radius: 14px;
    border: none;
    background: linear-gradient(#b07a3a, #8b5a2b);
    color: white;
    cursor: pointer;
}
</style>
</head>

<body>

<!-- 🎮 MENU -->
<div id="menu">
    <h1>Hallo 👋 Wähle dein Spiel</h1>
    <button class="menuBtn" onclick="startGame('forest')">🌲 Forest Run</button>
    <button class="menuBtn" onclick="startGame('beach')">🏖 Beach Run</button>
</div>

<canvas id="game" width="900" height="420"></canvas>

<div id="score">Score: 0</div>
<div id="level">Level: 1</div>

<div id="gameover">GAME OVER</div>
<button id="restart" onclick="resetGame()">Neustart</button>

<div id="ui">
    <button id="jumpBtn">⬆ SPRINGEN</button>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let mode = "forest";
let started = false;
let gameOver = false;

let player = {x:120,y:300,w:28,h:28,vy:0};
let gravity = 1.1;
let ground = 300;

let obstacles = [];
let clouds = [];
let birds = [];

let score = 0;
let level = 1;
let speed = 6;
let time = 0;

/* ---------------- START ---------------- */
function startGame(m){
    mode = m;
    started = true;
    document.getElementById("menu").style.display = "none";
}

/* ---------------- INPUT ---------------- */
function jump(){
    if(!started||gameOver) return;
    if(player.y>=ground) player.vy=-15;
}

document.getElementById("jumpBtn").onclick = jump;
document.addEventListener("keydown",e=>{
    if(e.code==="Space") jump();
});

/* ---------------- SPAWN ---------------- */
setInterval(()=>{
    if(started&&!gameOver){
        obstacles.push({x:900,y:320,w:40,h:40});
    }
},1500);

/* ---------------- UPDATE ---------------- */
function update(){
    if(!started||gameOver) return;

    time+=0.02;

    player.y+=player.vy;
    if(player.y<ground) player.vy+=gravity;
    else {player.y=ground;player.vy=0;}

    for(let o of obstacles) o.x-=speed;

    score++;
    level=Math.floor(score/500)+1;
    speed=6+level*0.5;

    document.getElementById("score").innerText="Score: "+Math.floor(score/10);
    document.getElementById("level").innerText="Level: "+level;

    obstacles = obstacles.filter(o=>o.x>-100);

    for(let o of obstacles){
        if(hit(o)) endGame();
    }
}

/* ---------------- COLLISION ---------------- */
function hit(o){
    return player.x<o.x+o.w &&
           player.x+player.w>o.x &&
           player.y<o.y+o.h &&
           player.y+player.h>o.y;
}

/* ---------------- DRAW ---------------- */
function draw(){

    ctx.clearRect(0,0,900,420);

    if(mode==="forest"){
        drawForest();
    } else {
        drawBeach();
    }

    drawGround();

    ctx.fillStyle="#ffd54a";
    ctx.fillRect(player.x,player.y,player.w,player.h);

    ctx.fillStyle="#7a4a1f";
    for(let o of obstacles){
        ctx.fillRect(o.x,o.y,o.w,o.h);
    }
}

/* ---------------- FOREST ---------------- */
function drawForest(){
    ctx.fillStyle="#87ceeb";
    ctx.fillRect(0,0,900,420);

    ctx.fillStyle="#1f3b2a";
    for(let i=0;i<18;i++){
        let x=i*60;
        ctx.fillRect(x,260,20,160);
    }
}

/* ---------------- BEACH ---------------- */
function drawBeach(){

    // sky
    ctx.fillStyle="#87ceeb";
    ctx.fillRect(0,0,900,260);

    // sea
    ctx.fillStyle="#1e90ff";
    ctx.fillRect(0,120,900,140);

    // sand
    ctx.fillStyle="#f4d03f";
    ctx.fillRect(0,260,900,160);
}

/* ---------------- GROUND ---------------- */
function drawGround(){
    if(mode==="forest"){
        ctx.fillStyle="#1a1f2e";
    } else {
        ctx.fillStyle="#f4d03f";
    }
    ctx.fillRect(0,340,900,80);
}

/* ---------------- GAME OVER ---------------- */
function endGame(){
    gameOver=true;
    document.getElementById("gameover").style.display="block";
    document.getElementById("restart").style.display="block";
}

/* ---------------- RESET ---------------- */
function resetGame(){
    location.reload();
}

/* ---------------- LOOP ---------------- */
function loop(){
    update();
    draw();
    requestAnimationFrame(loop);
}

loop();
</script>

</body>
</html>
"""

components.html(game_html, height=750)
