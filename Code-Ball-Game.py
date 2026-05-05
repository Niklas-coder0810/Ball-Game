import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Runner Forest Ultra", layout="wide")

st.title("🌲 Runner Forest Ultra (Day/Night System)")

game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>

<style>
body{
    margin:0;
    overflow:hidden;
    font-family:Arial;
    background:#111;
}

canvas{
    display:block;
    margin:auto;
    border-radius:14px;
    box-shadow:0 25px 60px rgba(0,0,0,0.6);
}

/* MENU */
#menu{
    position:absolute;
    width:900px;
    height:420px;
    left:50%;
    transform:translateX(-50%);
    top:20px;
    background:linear-gradient(#0b1020,#05060c);
    color:white;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    z-index:10;
    border-radius:12px;
}

/* UI */
#score,#level{
    position:absolute;
    top:10px;
    color:white;
    background:rgba(0,0,0,0.45);
    padding:8px 14px;
    border-radius:10px;
}

#score{left:20px;}
#level{right:20px;}

#gameover{
    position:absolute;
    top:35%;
    width:100%;
    text-align:center;
    font-size:60px;
    color:white;
    display:none;
}

/* BUTTONS */
#ui{
    position:absolute;
    top:460px;
    left:50%;
    transform:translateX(-50%);
}

button{
    padding:16px 32px;
    border:none;
    border-radius:12px;
    background:#8b5a2b;
    color:white;
    font-size:20px;
    cursor:pointer;
}
</style>

</head>

<body>

<div id="menu">
    <h1>🌲 Forest Run</h1>
    <button onclick="startGame()">Start</button>
</div>

<canvas id="game" width="900" height="420"></canvas>

<div id="score">Score: 0</div>
<div id="level">Level: 1</div>
<div id="gameover">GAME OVER</div>

<div id="ui">
    <button onclick="jump()">⬆ SPRINGEN</button>
</div>

<script>

/* =========================================================
   CORE STATE
========================================================= */

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let started = false;
let gameOver = false;

let time = 0;
let score = 0;
let level = 1;
let speed = 6;

let player = {
    x:120,
    y:300,
    w:28,
    h:28,
    vy:0
};

let gravity = 1.1;
let ground = 300;

let obstacles = [];

/* =========================================================
   START
========================================================= */

function startGame(){
    started = true;
    document.getElementById("menu").style.display="none";
}

/* =========================================================
   INPUT
========================================================= */

function jump(){
    if(!started || gameOver) return;
    if(player.y >= ground){
        player.vy = -15;
    }
}

/* =========================================================
   SPAWN
========================================================= */

setInterval(()=>{
    if(started && !gameOver){
        obstacles.push({x:900,y:320,w:40,h:40});
    }
},1500);

/* =========================================================
   UPDATE
========================================================= */

function update(){

    if(!started || gameOver) return;

    time += 0.02;

    player.y += player.vy;

    if(player.y < ground){
        player.vy += gravity;
    } else {
        player.y = ground;
        player.vy = 0;
    }

    for(let o of obstacles){
        o.x -= speed;
    }

    score++;
    level = Math.floor(score/500)+1;
    speed = 6 + level*0.5;

    document.getElementById("score").innerText = "Score: " + Math.floor(score/10);
    document.getElementById("level").innerText = "Level: " + level;

    for(let o of obstacles){
        if(hit(o)) gameOver = true;
    }

    obstacles = obstacles.filter(o=>o.x>-100);
}

/* =========================================================
   COLLISION
========================================================= */

function hit(o){
    return player.x<o.x+o.w &&
           player.x+player.w>o.x &&
           player.y<o.y+o.h &&
           player.y+player.h>o.y;
}

/* =========================================================
   DAY NIGHT SYSTEM
========================================================= */

function getDayPhase(){

    let t = time % 60;

    if(t < 20) return "night";
    if(t < 30) return "sunrise";
    if(t < 50) return "day";
    return "sunset";
}

/* =========================================================
   DRAW SKY
========================================================= */

function drawSky(){

    let phase = getDayPhase();

    if(phase === "night"){
        ctx.fillStyle = "#050817";
    }
    else if(phase === "sunrise"){
        ctx.fillStyle = "#ff9966";
    }
    else if(phase === "day"){
        ctx.fillStyle = "#87ceeb";
    }
    else{
        ctx.fillStyle = "#ff5e62";
    }

    ctx.fillRect(0,0,900,420);
}

/* =========================================================
   SUN + MOON
========================================================= */

function drawSunMoon(){

    let phase = getDayPhase();

    if(phase === "day" || phase === "sunrise" || phase === "sunset"){
        ctx.fillStyle = "yellow";
        ctx.beginPath();
        ctx.arc(750,80,30,0,Math.PI*2);
        ctx.fill();
    }

    if(phase === "night"){
        ctx.fillStyle = "#ddd";
        ctx.beginPath();
        ctx.arc(750,80,25,0,Math.PI*2);
        ctx.fill();
    }
}

/* =========================================================
   STARS
========================================================= */

function drawStars(){

    let phase = getDayPhase();
    if(phase !== "night") return;

    ctx.fillStyle = "white";

    for(let i=0;i<60;i++){
        let x = (i*70) % 900;
        let y = (i*30) % 200;
        ctx.fillRect(x,y,2,2);
    }
}

/* =========================================================
   CLOUDS
========================================================= */

function drawClouds(){

    let phase = getDayPhase();
    if(phase !== "day") return;

    ctx.fillStyle = "white";

    for(let i=0;i<5;i++){
        let x = (i*200 + time*20) % 900;
        ctx.beginPath();
        ctx.arc(x,80,20,0,Math.PI*2);
        ctx.arc(x+20,80,20,0,Math.PI*2);
        ctx.fill();
    }
}

/* =========================================================
   TREES (FIXED LOOK)
========================================================= */

function drawTrees(){

    for(let i=0;i<18;i++){

        let x = i*60;

        // trunk
        ctx.fillStyle = "#5b3a1a";
        ctx.fillRect(x+5,280,10,80);

        // leaves
        ctx.fillStyle = "#1f7a3a";
        ctx.beginPath();
        ctx.arc(x+10,260,25,0,Math.PI*2);
        ctx.fill();
    }
}

/* =========================================================
   DRAW
========================================================= */

function draw(){

    ctx.clearRect(0,0,900,420);

    drawSky();
    drawStars();
    drawClouds();
    drawSunMoon();
    drawTrees();

    // ground
    ctx.fillStyle = "#1a1f2e";
    ctx.fillRect(0,340,900,80);

    // player
    ctx.fillStyle = "yellow";
    ctx.fillRect(player.x,player.y,player.w,player.h);

    // eyes
    ctx.fillStyle = "black";
    ctx.fillRect(player.x+6,player.y+8,3,3);
    ctx.fillRect(player.x+16,player.y+8,3,3);

    // obstacles
    ctx.fillStyle="#7a4a1f";
    for(let o of obstacles){
        ctx.fillRect(o.x,o.y,o.w,o.h);
    }
}

/* =========================================================
   LOOP
========================================================= */

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
