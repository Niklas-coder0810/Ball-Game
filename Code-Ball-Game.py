import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Runner Ultimate+", layout="wide")

st.title("🌍 Runner Ultimate+ (Forest & Beach + Custom Cube)")

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
    align-items: center;
    justify-content: center;
    z-index: 10;
    border-radius: 12px;
}

.menuRow {
    margin: 10px;
}

/* ---------------- COLOR SELECT ---------------- */
.colorBtn {
    width: 30px;
    height: 30px;
    margin: 4px;
    border-radius: 50%;
    border: 2px solid white;
    cursor: pointer;
}

/* ---------------- UI ---------------- */
#score, #level {
    position: absolute;
    top: 10px;
    color: white;
    background: rgba(0,0,0,0.4);
    padding: 8px 14px;
    border-radius: 10px;
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

<!-- MENU -->
<div id="menu">
    <h1>🎮 Wähle Modus & Farbe</h1>

    <div class="menuRow">
        <button onclick="start('forest')">🌲 Forest Run</button>
        <button onclick="start('beach')">🏖 Beach Run</button>
    </div>

    <div class="menuRow">
        <div onclick="setColor('yellow')" class="colorBtn" style="background:yellow"></div>
        <div onclick="setColor('red')" class="colorBtn" style="background:red"></div>
        <div onclick="setColor('green')" class="colorBtn" style="background:green"></div>
        <div onclick="setColor('blue')" class="colorBtn" style="background:blue"></div>
        <div onclick="setColor('pink')" class="colorBtn" style="background:pink"></div>
        <div onclick="setColor('violet')" class="colorBtn" style="background:violet"></div>
        <div onclick="setColor('brown')" class="colorBtn" style="background:brown"></div>
    </div>
</div>

<canvas id="game" width="900" height="420"></canvas>

<div id="score">Score: 0</div>
<div id="level">Level: 1</div>

<div id="gameover">GAME OVER</div>
<button id="restart" onclick="resetGame()">Neustart</button>

<div id="ui">
    <button onclick="jump()">⬆ SPRINGEN</button>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let mode = "forest";
let cubeColor = "yellow";

let started = false;
let gameOver = false;

let player = {x:120,y:300,w:28,h:28,vy:0};

let obstacles = [];
let score = 0;
let level = 1;
let speed = 6;
let time = 0;

/* ---------------- MENU ---------------- */
function start(m){
    mode = m;
    started = true;
    document.getElementById("menu").style.display="none";
}

function setColor(c){
    cubeColor = c;
}

/* ---------------- INPUT ---------------- */
function jump(){
    if(!started||gameOver) return;
    if(player.y>=300) player.vy=-15;
}

/* ---------------- SPAWN ---------------- */
setInterval(()=>{
    if(started && !gameOver){
        obstacles.push({x:900,y:320,w:40,h:40});
    }
},1500);

/* ---------------- UPDATE ---------------- */
function update(){
    if(!started||gameOver) return;

    time+=0.02;

    player.y+=player.vy;
    if(player.y<300) player.vy+=1.1;
    else {player.y=300;player.vy=0;}

    for(let o of obstacles) o.x-=speed;

    score++;
    level=Math.floor(score/500)+1;
    speed=6+level*0.5;

    document.getElementById("score").innerText="Score: "+Math.floor(score/10);
    document.getElementById("level").innerText="Level: "+level;

    obstacles = obstacles.filter(o=>o.x>-100);

    for(let o of obstacles){
        if(hit(o)) gameOver=true;
    }
}

/* ---------------- HIT ---------------- */
function hit(o){
    return player.x<o.x+o.w &&
           player.x+player.w>o.x &&
           player.y<o.y+o.h &&
           player.y+player.h>o.y;
}

/* ---------------- DRAW ---------------- */
function draw(){
    ctx.clearRect(0,0,900,420);

    if(mode==="forest") drawForest();
    else drawBeach();

    ctx.fillStyle=cubeColor;
    ctx.fillRect(player.x,player.y,player.w,player.h);

    ctx.fillStyle="#7a4a1f";
    for(let o of obstacles){
        ctx.fillRect(o.x,o.y,o.w,o.h);
    }
}

/* ---------------- FOREST + NIGHT/DAY ---------------- */
function drawForest(){
    let phase = Math.floor((time%60)/20);

    if(phase===0) ctx.fillStyle="#050817"; // night
    else ctx.fillStyle="#87ceeb";

    ctx.fillRect(0,0,900,420);

    // trees FIXED
    for(let i=0;i<18;i++){
        let x=i*60;
        ctx.fillStyle = (phase===0) ? "#0b0f14" : "#1f3b2a";
        ctx.fillRect(x,260,20,160);
        ctx.beginPath();
        ctx.arc(x+10,260,25,0,Math.PI*2);
        ctx.fill();
    }
}

/* ---------------- BEACH + WAVES + SUN FACE ---------------- */
function drawBeach(){

    ctx.fillStyle="#87ceeb";
    ctx.fillRect(0,0,900,220);

    // sun with face
    ctx.fillStyle="yellow";
    ctx.beginPath();
    ctx.arc(750,80,35,0,Math.PI*2);
    ctx.fill();

    ctx.fillStyle="black";
    ctx.fillRect(740,75,5,5);
    ctx.fillRect(760,75,5,5);

    // smile
    ctx.beginPath();
    ctx.arc(750,85,10,0,Math.PI);
    ctx.stroke();

    // waves animation
    ctx.fillStyle="#1e90ff";
    for(let i=0;i<900;i+=40){
        let wave = Math.sin((time*5)+(i*0.02))*5;
        ctx.fillRect(i,220+wave,40,100);
    }

    // sand
    ctx.fillStyle="#f4d03f";
    ctx.fillRect(0,320,900,100);
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
