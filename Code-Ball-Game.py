import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Runner Full Stable", layout="wide")

st.title("🌍 Runner Full Stable Edition (Forest + Beach + Safe Architecture)")

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

/* CANVAS */
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

.menuRow{
    margin:10px;
}

.colorBtn{
    width:28px;
    height:28px;
    border-radius:50%;
    display:inline-block;
    margin:4px;
    cursor:pointer;
    border:2px solid white;
}

/* UI */
#score,#level,#highscore{
    position:absolute;
    top:10px;
    color:white;
    background:rgba(0,0,0,0.45);
    padding:8px 14px;
    border-radius:10px;
    font-weight:bold;
}

#score{left:20px;}
#level{right:20px;}
#highscore{left:20px; top:60px;}

#gameover{
    position:absolute;
    top:35%;
    width:100%;
    text-align:center;
    font-size:60px;
    color:white;
    display:none;
}

button{
    padding:14px 26px;
    margin:8px;
    border:none;
    border-radius:12px;
    background:#8b5a2b;
    color:white;
    cursor:pointer;
}
</style>

</head>

<body>

<!-- MENU -->
<div id="menu">
    <h1>🎮 Runner Game</h1>

    <div class="menuRow">
        <button onclick="startGame('forest')">🌲 Forest</button>
        <button onclick="startGame('beach')">🏖 Beach</button>
    </div>

    <div class="menuRow">
        <div class="colorBtn" style="background:yellow" onclick="setColor('yellow')"></div>
        <div class="colorBtn" style="background:red" onclick="setColor('red')"></div>
        <div class="colorBtn" style="background:green" onclick="setColor('green')"></div>
        <div class="colorBtn" style="background:blue" onclick="setColor('blue')"></div>
        <div class="colorBtn" style="background:pink" onclick="setColor('pink')"></div>
        <div class="colorBtn" style="background:violet" onclick="setColor('violet')"></div>
        <div class="colorBtn" style="background:brown" onclick="setColor('brown')"></div>
    </div>
</div>

<canvas id="game" width="900" height="420"></canvas>

<div id="score">Score: 0</div>
<div id="level">Level: 1</div>
<div id="highscore">Highscore: 0</div>

<div id="gameover">GAME OVER</div>

<script>

/* =========================================================
   🧠 GAME CORE STATE (DO NOT TOUCH)
========================================================= */

const canvas=document.getElementById("game");
const ctx=canvas.getContext("2d");

let mode="forest";
let started=false;
let gameOver=false;

let time=0;
let score=0;
let level=1;
let speed=6;

let player={
    x:120,
    y:300,
    w:28,
    h:28,
    vy:0,
    color:"yellow"
};

let gravity=1.1;
let ground=300;

/* =========================================================
   🌍 WORLD OBJECTS
========================================================= */

let obstacles=[];
let birds=[];
let clouds=[];

/* =========================================================
   🎮 MENU FUNCTIONS
========================================================= */

function startGame(m){
    mode=m;
    started=true;
    document.getElementById("menu").style.display="none";
}

function setColor(c){
    player.color=c;
}

/* =========================================================
   🎮 INPUT
========================================================= */

document.addEventListener("keydown",e=>{
    if(e.code==="Space") jump();
});

function jump(){
    if(!started||gameOver) return;
    if(player.y>=ground){
        player.vy=-15;
    }
}

/* =========================================================
   📦 SPAWN SYSTEM (SAFE ADDITION)
========================================================= */

setInterval(()=>{
    if(started && !gameOver){
        obstacles.push({
            x:900,
            y:320,
            w:40,
            h:40
        });
    }
},1500);

/* =========================================================
   🧠 UPDATE ENGINE
========================================================= */

function update(){

    if(!started||gameOver) return;

    time+=0.02;

    // player physics
    player.y+=player.vy;

    if(player.y<ground){
        player.vy+=gravity;
    } else {
        player.y=ground;
        player.vy=0;
    }

    // move obstacles
    for(let o of obstacles){
        o.x-=speed;
    }

    // difficulty scaling
    score++;
    level=Math.floor(score/500)+1;
    speed=6+level*0.5;

    // UI
    document.getElementById("score").innerText="Score: "+Math.floor(score/10);
    document.getElementById("level").innerText="Level: "+level;
    document.getElementById("highscore").innerText="Highscore: "+(localStorage.getItem("hs")||0);

    // collisions
    for(let o of obstacles){
        if(hit(o)){
            endGame();
        }
    }

    obstacles=obstacles.filter(o=>o.x>-100);
}

/* =========================================================
   💥 COLLISION
========================================================= */

function hit(o){
    return player.x<o.x+o.w &&
           player.x+player.w>o.x &&
           player.y<o.y+o.h &&
           player.y+player.h>o.y;
}

/* =========================================================
   🎨 RENDER SYSTEM
========================================================= */

function draw(){

    ctx.clearRect(0,0,900,420);

    if(mode==="forest") drawForest();
    else drawBeach();

    drawGround();
    drawPlayer();

    ctx.fillStyle="#7a4a1f";
    for(let o of obstacles){
        ctx.fillRect(o.x,o.y,o.w,o.h);
    }
}

/* =========================================================
   🌲 FOREST (FIXED BÄUME + TAG/NACHT)
========================================================= */

function drawForest(){

    let phase=Math.floor((time%60)/20);

    if(phase===0){
        ctx.fillStyle="#050817"; // night
    } else {
        ctx.fillStyle="#87ceeb"; // day
    }

    ctx.fillRect(0,0,900,420);

    // trees FIXED clean style
    for(let i=0;i<18;i++){
        let x=i*60;

        ctx.fillStyle=(phase===0)?"#0b0f14":"#1f3b2a";
        ctx.fillRect(x,260,18,160);

        ctx.beginPath();
        ctx.arc(x+9,260,28,0,Math.PI*2);
        ctx.fill();
    }
}

/* =========================================================
   🏖 BEACH (WAVES + SUN FACE)
========================================================= */

function drawBeach(){

    // sky
    ctx.fillStyle="#87ceeb";
    ctx.fillRect(0,0,900,220);

    // sun face
    ctx.fillStyle="yellow";
    ctx.beginPath();
    ctx.arc(750,80,30,0,Math.PI*2);
    ctx.fill();

    ctx.fillStyle="black";
    ctx.fillRect(742,75,4,4);
    ctx.fillRect(756,75,4,4);

    ctx.beginPath();
    ctx.arc(750,85,10,0,Math.PI);
    ctx.stroke();

    // waves
    ctx.fillStyle="#1e90ff";
    for(let i=0;i<900;i+=40){
        let wave=Math.sin(time*4+i*0.02)*6;
        ctx.fillRect(i,220+wave,40,120);
    }

    // sand
    ctx.fillStyle="#f4d03f";
    ctx.fillRect(0,320,900,100);
}

/* =========================================================
   🌍 GROUND
========================================================= */

function drawGround(){
    ctx.fillStyle = (mode==="forest") ? "#1a1f2e" : "#f4d03f";
    ctx.fillRect(0,340,900,80);
}

/* =========================================================
   👤 PLAYER (WITH EYES FIXED)
========================================================= */

function drawPlayer(){

    ctx.fillStyle=player.color;
    ctx.fillRect(player.x,player.y,player.w,player.h);

    // eyes ALWAYS visible
    ctx.fillStyle="black";
    ctx.fillRect(player.x+6,player.y+8,3,3);
    ctx.fillRect(player.x+16,player.y+8,3,3);
}

/* =========================================================
   💀 GAME OVER
========================================================= */

function endGame(){
    gameOver=true;

    let hs=localStorage.getItem("hs")||0;
    if(score>hs){
        localStorage.setItem("hs",score);
    }

    document.getElementById("gameover").style.display="block";
}

/* =========================================================
   🔁 LOOP
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
