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

/* SPAWN */
setInterval(()=>{
    if(started&&!gameOver){
        obstacles.push({x:900,y:320,w:40,h:40});
    }
},1500);

/* UPDATE */
function update(){
    if(!started||gameOver) return;

    time+=0.02;

    player.y+=player.vy;
    if(player.y<ground) player.vy+=gravity;
    else {player.y=ground;player.vy=0;}

    obstacles.forEach(o=>o.x-=speed);

    score++;
    level=Math.floor(score/500)+1;
    speed=6+level*0.5;

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

/* DAY SYSTEM */
function phase(){
    let t=time%60;
    if(t<20) return "night";
    if(t<30) return "sunrise";
    if(t<50) return "day";
    return "sunset";
}

/* SKY */
function drawSky(){
    let p=phase();
    if(p==="night") ctx.fillStyle="#050817";
    else if(p==="sunrise") ctx.fillStyle="#ff9966";
    else if(p==="day") ctx.fillStyle="#87ceeb";
    else ctx.fillStyle="#ff5e62";

    ctx.fillRect(0,0,900,420);
}

/* CLOUDS */
function drawClouds(){
    let p=phase();

    if(p==="night") ctx.fillStyle="rgba(200,200,255,0.2)";
    else if(p==="sunrise"||p==="sunset") ctx.fillStyle="rgba(255,200,150,0.5)";
    else ctx.fillStyle="white";

    for(let i=0;i<6;i++){
        let x=(i*180+time*15)%900;
        ctx.beginPath();
        ctx.arc(x,90,18,0,Math.PI*2);
        ctx.arc(x+20,90,18,0,Math.PI*2);
        ctx.fill();
    }
}

/* STARS */
function drawStars(){
    if(phase()!=="night") return;

    ctx.fillStyle="white";
    for(let i=0;i<60;i++){
        let x=(i*70)%900;
        let y=(i*30)%200;
        ctx.fillRect(x,y,2,2);
    }
}

/* SUN/MOON */
function drawSunMoon(){
    let p=phase();

    if(p==="night"){
        ctx.fillStyle="#ddd";
        ctx.beginPath();
        ctx.arc(750,80,25,0,Math.PI*2);
        ctx.fill();
    } else {
        ctx.fillStyle="yellow";
        ctx.beginPath();
        ctx.arc(750,80,30,0,Math.PI*2);
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
    drawStars();
    drawClouds();
    drawSunMoon();
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
