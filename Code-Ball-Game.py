import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Forest Runner", layout="wide")

game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>

<style>
body { margin:0; overflow:hidden; background:#111; font-family:Arial; }

canvas {
    display:block;
    margin:auto;
    border-radius:14px;
}

/* MENU */
#menu{
    position:absolute;
    width:900px;
    height:420px;
    left:50%;
    transform:translateX(-50%);
    top:20px;
    background:#0b1020;
    color:white;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
}

/* COLOR PICKER */
#colorPicker{
    display:flex;
    gap:10px;
    margin-top:10px;
}

.colorChoice{
    width:35px;
    height:35px;
    border-radius:50%;
    border:3px solid transparent;
    cursor:pointer;
}

.colorSelected{
    border:3px solid white;
    transform:scale(1.2);
}

/* UI */
#score,#level{
    position:absolute;
    top:10px;
    color:white;
    background:rgba(0,0,0,0.4);
    padding:8px;
    border-radius:8px;
}

#score{left:20px;}
#level{right:20px;}

#gameover{
    position:absolute;
    top:35%;
    width:100%;
    text-align:center;
    font-size:50px;
    color:white;
    display:none;
}

/* BUTTONS */
#ui{
    position:absolute;
    top:460px;
    width:100%;
    text-align:center;
}

button{
    padding:14px 28px;
    border:none;
    border-radius:10px;
    background:#8b5a2b;
    color:white;
    font-size:18px;
    cursor:pointer;
}

#restartBtn{
    position:absolute;
    top:55%;
    left:50%;
    transform:translateX(-50%);
    display:none;
    background:#ffd54a;
}
</style>
</head>

<body>

<div id="menu">
    <h1>🌲 Forest Run</h1>

    <h3>Wähle deine Farbe</h3>
    <div id="colorPicker">
        <div class="colorChoice colorSelected" data-color="yellow" style="background:yellow"></div>
        <div class="colorChoice" data-color="green" style="background:green"></div>
        <div class="colorChoice" data-color="red" style="background:red"></div>
        <div class="colorChoice" data-color="blue" style="background:blue"></div>
        <div class="colorChoice" data-color="pink" style="background:pink"></div>
    </div>

    <button onclick="startGame()">Start</button>
</div>

<canvas id="game" width="900" height="420"></canvas>

<div id="score">Score: 0</div>
<div id="level">Level: 1</div>

<div id="gameover">GAME OVER</div>
<button id="restartBtn" onclick="resetGame()">Neustart</button>

<div id="ui">
    <button onclick="jump()">⬆ SPRINGEN</button>
</div>

<script>

/* STATE */
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let started=false;
let gameOver=false;

let time=0;
let score=0;
let level=1;
let speed=6;

let player={
    x:120,y:300,w:28,h:28,vy:0,color:"yellow"
};

let obstacles=[];
let gravity=1.1;
let ground=300;

/* COLOR PICKER */
document.querySelectorAll(".colorChoice").forEach(btn=>{
    btn.onclick=()=>{
        document.querySelectorAll(".colorChoice").forEach(b=>b.classList.remove("colorSelected"));
        btn.classList.add("colorSelected");
        player.color=btn.dataset.color;
    };
});

/* START */
function startGame(){
    started=true;
    document.getElementById("menu").style.display="none";
}

/* INPUT */
function jump(){
    if(!started||gameOver) return;
    if(player.y>=ground) player.vy=-15;
}

/* RANDOM SPAWN SYSTEM */
let spawnTimer = 60;

function updateSpawning(){

    spawnTimer--;

    if(spawnTimer <= 0){

        obstacles.push({
            x:900,
            y:320,
            w:40,
            h:40
        });

        // zufällige Abstände + schwieriger mit Level
        spawnTimer = Math.max(20, 60 + Math.random()*100 - level*5);
    }
}

/* UPDATE */
function update(){
    if(!started||gameOver) return;

    time+=0.02;

    updateSpawning();

    player.y+=player.vy;
    if(player.y<ground) player.vy+=gravity;
    else {player.y=ground;player.vy=0;}

    obstacles.forEach(o=>o.x-=speed);

    score++;

    // Schwierigkeit alle 100 Punkte
    level = Math.floor(score/100) + 1;
    speed = 6 + level * 0.7;

    document.getElementById("score").innerText="Score: "+Math.floor(score/10);
    document.getElementById("level").innerText="Level: "+level;

    obstacles.forEach(o=>{
        if(hit(o)) endGame();
    });

    obstacles=obstacles.filter(o=>o.x>-100);
}

/* COLLISION */
function hit(o){
    return player.x<o.x+o.w &&
           player.x+player.w>o.x &&
           player.y<o.y+o.h &&
           player.y+player.h>o.y;
}

/* SMOOTH SKY */
function lerpColor(a,b,t){
    let ar=parseInt(a.substr(1,2),16);
    let ag=parseInt(a.substr(3,2),16);
    let ab=parseInt(a.substr(5,2),16);

    let br=parseInt(b.substr(1,2),16);
    let bg=parseInt(b.substr(3,2),16);
    let bb=parseInt(b.substr(5,2),16);

    let rr=Math.floor(ar+(br-ar)*t);
    let rg=Math.floor(ag+(bg-ag)*t);
    let rb=Math.floor(ab+(bb-ab)*t);

    return "rgb("+rr+","+rg+","+rb+")";
}

function drawSky(){

    let t=time%60;
    let color;

    if(t<20){
        color=lerpColor("#050817","#ff9966",t/20);
    }
    else if(t<30){
        color=lerpColor("#ff9966","#87ceeb",(t-20)/10);
    }
    else if(t<50){
        color="#87ceeb";
    }
    else{
        color=lerpColor("#ff5e62","#050817",(t-50)/10);
    }

    ctx.fillStyle=color;
    ctx.fillRect(0,0,900,420);
}

/* CLOUDS */
function drawClouds(){
    ctx.fillStyle="rgba(255,255,255,0.5)";
    for(let i=0;i<6;i++){
        let x=(i*180+time*15)%900;
        ctx.beginPath();
        ctx.arc(x,90,18,0,Math.PI*2);
        ctx.arc(x+20,90,18,0,Math.PI*2);
        ctx.fill();
    }
}

/* TREES */
function drawTrees(){
    for(let i=0;i<18;i++){
        let x=i*60;

        ctx.fillStyle="#5b3a1a";
        ctx.fillRect(x+5,280,10,80);

        ctx.fillStyle="#1f7a3a";
        ctx.beginPath();
        ctx.arc(x+10,260,25,0,Math.PI*2);
        ctx.fill();
    }
}

/* DRAW */
function draw(){
    ctx.clearRect(0,0,900,420);

    drawSky();
    drawClouds();
    drawTrees();

    ctx.fillStyle="#1a1f2e";
    ctx.fillRect(0,340,900,80);

    ctx.fillStyle=player.color;
    ctx.fillRect(player.x,player.y,player.w,player.h);

    ctx.fillStyle="black";
    ctx.fillRect(player.x+6,player.y+8,3,3);
    ctx.fillRect(player.x+16,player.y+8,3,3);

    ctx.fillStyle="#7a4a1f";
    obstacles.forEach(o=>{
        ctx.fillRect(o.x,o.y,o.w,o.h);
    });
}

/* GAME OVER */
function endGame(){
    gameOver=true;
    document.getElementById("gameover").style.display="block";
    document.getElementById("restartBtn").style.display="block";
}

/* RESET */
function resetGame(){
    gameOver=false;
    score=0;
    level=1;
    speed=6;
    obstacles=[];
    player.y=ground;
    player.vy=0;

    document.getElementById("gameover").style.display="none";
    document.getElementById("restartBtn").style.display="none";
}

/* LOOP */
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
