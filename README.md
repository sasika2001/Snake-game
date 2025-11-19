<!doctype html>
<html lang="en">

<head>
<meta charset="utf-8">
<title>MULTI AGENT SNAKE ARENA — README</title>

<style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial;
        line-height: 1.6;
        color: #111;
        padding: 24px;
        max-width: 1000px;
        margin: auto;
        background: #f7f8fb;
    }

    header {
        background: linear-gradient(90deg, #0f172a, #0b1220);
        color: white;
        padding: 22px;
        border-radius: 12px;
        margin-bottom: 20px;
    }

    header h1 {
        margin: 0;
        font-size: 28px;
    }

    .meta {
        margin-top: 5px;
        font-size: 14px;
        color: #cbd5e1;
    }

    section {
        background: white;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: 16px;
        box-shadow: 0 6px 18px rgba(12, 15, 30, 0.06);
    }

    pre {
        background: #0b1220;
        color: #dbeafe;
        padding: 12px;
        border-radius: 8px;
        overflow-x: auto;
    }

    .grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
    }

    img.sshot {
        width: 100%;
        border-radius: 8px;
        border: 1px solid #e6eef8;
    }

    @media(max-width:800px) {
        .grid {
            grid-template-columns: 1fr;
        }
    }
</style>
</head>


<body>

<header>
    <h1>MULTI AGENT SNAKE ARENA</h1>
    <p class="meta">A multi-agent snake arena demonstrating agentic behavior, emergent complexity & interactive dynamics.<br>
    By <strong>Sasika Sewmini</strong> — Index <strong>225532T</strong></p>
</header>

<section>
<h2>About</h2>
<p>
Multi Agent Snake Arena is an extended snake game built to showcase multiple interacting agents: AI-controlled snakes,
a human-controlled snake, food agents, obstacle agents, and environmental rule-based behaviors.

It explores concepts such as:
<strong>rational agents, perception, decision-making, complex systems,
emergent behavior, emergency handling, and agent coordination</strong>.
</p>
</section>

<section>
<h2>Game Elements & Colors</h2>

<ul>
    <li><strong>Human Snake:</strong> <span style="color:green; font-weight:bold;">Green</span></li>
    <li><strong>AI Snake:</strong> <span style="color:red; font-weight:bold;">Red</span></li>
    <li><strong>Normal Food:</strong> <span style="color:gold; font-weight:bold;">Yellow</span> (+2)</li>
    <li><strong>Poison:</strong> <span style="color:hotpink; font-weight:bold;">Pink</span> (−4)</li>
    <li><strong>Bonus Food:</strong> <span style="color:#38bdf8; font-weight:bold;">Light Blue</span> (+6)</li>
</ul>

</section>

<section>
<h2>Key Features</h2>
<ul>
    <li>Multiple agent types (AI snake, player snake, food agents, obstacle agents).</li>
    <li>Rational agents with goal-oriented decision-making.</li>
    <li>Emergent behavior from simple rules (competition, avoidance, pattern formation).</li>
    <li>Emergency feature for critical events (collision risk, starvation, etc.).</li>
    <li>Pygame visualization with overlays and debugging tools.</li>
    <li>Configurable speed, arena size, reward rules & agent count.</li>
</ul>
</section>

<section>
<h2>Agentic Features (Detailed)</h2>
<ul>
    <li><strong>Perception:</strong> Agents sense nearby tiles (N, S, E, W + diagonals).</li>
    <li><strong>Internal State:</strong> Hunger, survival time, intended path.</li>
    <li><strong>Decision-Making:</strong> Rule-based or heuristic-driven movement.</li>
    <li><strong>Goal-Oriented:</strong> Food seeking, survival, or maximizing score.</li>
    <li><strong>Coordination & Competition:</strong> Indirect interaction via shared environment.</li>
    <li><strong>Emergency Handling:</strong> Rapid re-evaluation when danger is detected.</li>
</ul>
</section>

<section>
<h2>Tech Stack</h2>
<ul>
    <li>Python 3.10+</li>
    <li>Pygame</li>
    <li>NumPy</li>
</ul>
<p>Optional: Reinforcement learning integration (Stable-Baselines3, PyTorch)</p>
</section>

<section>
<h2>Installation</h2>
<pre>
# Clone repository
git clone &lt;your-repo-url&gt;
cd multi-agent-snake-arena

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
</pre>
</section>

<section>
<h2>Controls</h2>
<ul>
    <li>Move: Arrow keys or WASD</li>
    <li>Pause: Space or P</li>
    <li>Debug info: D</li>
    <li>Speed control: + / -</li>
</ul>
</section>

<section>
<h2>Project Structure</h2>
<pre>
multi-agent-snake-arena/
├─ README.html
├─ main.py
├─ core/
│  ├─ config.py
│  ├─ engine.py
│  └─ renderer.py
├─ agents/
│  ├─ base_agent.py
│  ├─ snake_agent.py
│  ├─ food_agent.py
│  └─ obstacle_agent.py
├─ assets/
│  └─ screenshots/
└─ requirements.txt
</pre>
</section>

<section>
<h2>Screenshots</h2>
<div class="grid">
    <img class="sshot" src="assets/screenshots/s1.png" alt="Screenshot 1">
    <img class="sshot" src="assets/screenshots/s2.png" alt="Screenshot 2">
</div>
</section>

<section>
<h2>Contact</h2>
<p>
<strong>Sasika Sewmini</strong><br>
Index Number: 225532T<br>
(Add email or GitHub link here)
</p>
</section>

<footer>
    MULTI AGENT SNAKE ARENA — README
</footer>

</body>
</html>
