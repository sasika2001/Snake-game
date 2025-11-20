<h1>🐍 Multi-Agent Snake Arena (MAS Project)</h1>

<p>
Multi-Agent Snake Arena is a Python-based simulation where multiple autonomous agents 
(Human Snake, AI Snakes, Food Agents, Obstacle Agents, and Bonus Agents) interact inside 
a dynamic environment. The game demonstrates core <b>Multi-Agent System (MAS)</b> concepts 
such as autonomy, reactivity, proactiveness, rationality, cooperation, competition, 
complex-system behaviour, and emergent outcomes.
</p>

<hr>

<h2> Game Overview</h2>
<p>The arena contains several agents that interact with each other in real time. The 
environment is fully dynamic, adaptive, and unpredictable—resulting in emergent behaviour.</p>

<ul>
    <li><b>Player controls the Human Snake</b> using arrow keys.</li>
    <li><b>AI Snakes</b> independently navigate, collect food, avoid obstacles, and compete.</li>
    <li><b>Food, Poison & Bonus agents</b> spawn randomly, affecting the score.</li>
</ul>

<hr>

<h2> Game Elements & Colors</h2>

<table border="1" cellpadding="8">
<tr>
    <th>Element / Agent</th>
    <th>Color</th>
    <th>Effect / Description</th>
</tr>

<tr>
    <td><b>Human Player Snake</b></td>
    <td style="background: #00aa00; color: white;">Green</td>
    <td>Controlled by the player. Main agent.</td>
</tr>

<tr>
    <td><b>AI Snakes</b></td>
    <td style="background: purple; color: white;">Purple</td>
    <td>Autonomous agents with decision-making logic.</td>
</tr>

<tr>
    <td><b>Normal Food</b></td>
    <td style="background: yellow;">Yellow</td>
    <td>Increases score by <b>+2</b></td>
</tr>

<tr>
    <td><b>Poison</b></td>
    <td style="background: pink;">Pink</td>
    <td>Reduces score by <b>-4</b></td>
</tr>

<tr>
    <td><b>Bonus Food</b></td>
    <td style="background: #66ccff;">Light Blue</td>
    <td>Increases score by <b>+6</b></td>
</tr>

<tr>
    <td><b>Obstacles</b></td>
    <td style="background: gray; color: white;">Gray</td>
    <td>Must be avoided; collision ends the game.</td>
</tr>
</table>

<hr>

<h2>Agentic Features (MAS Concepts)</h2>

<ul>
    <li><b>Autonomy</b> – Each AI snake behaves independently without human control.</li>
    <li><b>Reactivity</b> – Agents sense the environment and respond (food, poison, danger).</li>
    <li><b>Proactiveness</b> – AI snakes plan movements to maximize survival and score.</li>
    <li><b>Rationality</b> – Agents choose the best action based on goals (avoid death, get points).</li>
    <li><b>Cooperation</b> – Indirect collaboration by sharing space and reacting to each other.</li>
    <li><b>Competition</b> – Multiple snakes race for food and territory.</li>
    <li><b>Learning Elements (optional)*</b> – Can be extended for Q-learning or heuristics.</li>
    <li><b>Complex System Behaviour</b> – Many simple agents create unpredictable outcomes.</li>
    <li><b>Butterfly Effect</b> – A small early action (one food pickup) can change the final outcome drastically.</li>
</ul>

<hr>

<h2>Technologies Used</h2>
<ul>
    <li>Python</li>
    <li>Pygame</li>
    <li>OOP + Multi-Agent System Design</li>
</ul>

<hr>

<hr>

<h2> How to Run</h2>

<pre>
pip install pygame
python main.py
</pre>

<hr>

<h2> Key Features</h2>
<ul>
    <li>Multiple autonomous agents</li>
    <li>Competitive + cooperative multi-agent interactions</li>
    <li>Dynamic scoring system</li>
    <li>Color-based agent visualization</li>
    <li>Emergent complex-system behaviour</li>
    <li>AI snakes with autonomous decisions</li>
</ul>

<hr>

<h2> License</h2>
<p>This project is open-source. You may modify and use it freely.</p>

</body>
</html>
