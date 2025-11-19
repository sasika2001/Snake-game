<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>MULTI AGENT SNAKE ARENA — README</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial; line-height:1.6; color:#111; padding:24px; max-width:1000px; margin:auto; background:#f7f8fb; }
    header { background:linear-gradient(90deg,#0f172a,#0b1220); color:white; padding:20px; border-radius:12px; margin-bottom:20px; }
    h1 { margin:0; font-size:28px; }
    .meta { margin-top:6px; color:#cbd5e1; font-size:14px; }
    section { background:white; padding:18px; border-radius:10px; box-shadow:0 6px 18px rgba(12,15,30,0.06); margin-bottom:16px; }
    pre { background:#0b1220; color:#dbeafe; padding:12px; border-radius:8px; overflow:auto; }
    .grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
    .badge { display:inline-block; padding:6px 10px; border-radius:999px; background:#eef2ff; color:#3730a3; font-weight:600; font-size:13px; margin-right:8px; }
    .small { font-size:13px; color:#475569; }
    footer { text-align:center; color:#64748b; font-size:13px; margin-top:12px; }
    img.sshot { width:100%; border-radius:8px; border:1px solid #e6eef8; }
    @media (max-width:800px){ .grid{grid-template-columns:1fr} }
  </style>
</head>
<body>
  <header>
    <h1>MULTI AGENT SNAKE ARENA</h1>
    <div class="meta">A multi-agent snake arena demonstrating agentic behavior, emergent complexity, and interaction among agents — by <strong>Sasika Sewmini</strong> (Index: 225532T)</div>
  </header>

  <section>
    <h2>About</h2>
    <p>
      <strong>Multi Agent Snake Arena</strong> is an extended snake game built to showcase multiple interacting agents:
      autonomous AI-controlled snakes, food agents, obstacle agents and environmental rules. The project explores agentic features such as
      perception, decision-making (rational agents), resource competition, emergent behaviors, and an emergency handling mechanism.
    </p>
  </section>

  <section>
    <h2>Key features</h2>
    <ul>
      <li><strong>Multiple agent types:</strong> AI Snake Agents, Player-controlled Snake, Food Agents, Obstacle Agents.</li>
      <li><strong>Rational agents:</strong> Agent decision-making driven by heuristics or ML policies for seeking food and avoiding collisions.</li>
      <li><strong>Emergent behavior:</strong> Complex group dynamics (competition, avoidance) resulting from simple local rules.</li>
      <li><strong>Emergency feature:</strong> When critical events occur (e.g., imminent collision or starvation), agents trigger an emergency protocol to re-plan or prioritize survival actions.</li>
      <li><strong>Visualization:</strong> Pygame-based arena showing agent movements, state overlay and debugging info.</li>
      <li><strong>Configurable:</strong> adjustable agent counts, speed, arena size and reward rules for experiments.</li>
    </ul>
  </section>

  <section>
    <h2>Agentic features (detailed)</h2>
    <ul>
      <li><strong>Perception:</strong> agents sense local cells/tiles around them (N, S, E, W and diagonals up to a configurable range).</li>
      <li><strong>State & memory:</strong> each agent has internal state (hunger, steps survived, target coordinates).</li>
      <li><strong>Decision-making:</strong> rule-based heuristics or trained policies decide the next action (move direction, evade, chase).</li>
      <li><strong>Goal-oriented behavior:</strong> agents prioritize food collection, survival, or score-maximization depending on configuration.</li>
      <li><strong>Coordination & competition:</strong> agents interact indirectly via shared environment (food consumption, obstacles), producing emergent patterns.</li>
      <li><strong>Emergency handling:</strong> emergency events (e.g., predicted collision in < 2 steps or low energy) cause immediate re-evaluation of actions and may override normal goals.</li>
    </ul>
  </section>

  <section>
    <h2>Tech stack</h2>
    <div class="grid">
      <div>
        <span class="badge">Python 3.10+</span>
        <span class="badge">Pygame</span>
        <span class="badge">NumPy</span>
      </div>
      <div class="small">
        <p>Optional: You can plug in reinforcement learning libraries (stable-baselines3, PyTorch) if you want learning-based agents. Visualization and debugging overlays are implemented with Pygame.</p>
      </div>
    </div>
  </section>

  <section>
    <h2>Installation</h2>
    <p class="small">Assumes a typical Python environment. Adjust commands for your OS as needed.</p>

    <pre>
# clone the repo
git clone &lt;your-repo-url&gt;
cd multi-agent-snake-arena

# create a venv and activate it
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run the game
python main.py
    </pre>
    <p class="small">If you don't have a <code>requirements.txt</code>, create one with:</p>
    <pre>
pygame
numpy
    </pre>
  </section>

  <section>
    <h2>How to play / Controls</h2>
    <ul>
      <li><strong>Player snake controls:</strong> Arrow keys or WASD to move (configurable in <code>config.py</code>).</li>
      <li><strong>Start / Pause:</strong> <code>Space</code> or <code>P</code> (implementation-specific)</li>
      <li><strong>Toggle debug overlays:</strong> <code>D</code> (shows agent states, sensors)</li>
      <li><strong>Adjust simulation speed:</strong> +/- keys or GUI slider (if included)</li>
    </ul>
  </section>

  <section>
    <h2>Project structure (example)</h2>
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
├─ experiments/
│  └─ train_policy.py
├─ assets/
│  └─ sprites/
└─ requirements.txt
    </pre>
  </section>

  <section>
    <h2>Typical experiments & knobs</h2>
    <ul>
      <li>Vary agent counts (e.g., multiple AI snakes vs single player) to watch emergent competition.</li>
      <li>Enable learning agents to train policies that maximize survival/time-to-death.</li>
      <li>Tune emergency thresholds (how soon to trigger emergency avoidance) and observe behavior changes.</li>
      <li>Log metrics: collisions, food collected per agent, survival time, average path length.</li>
    </ul>
  </section>

  <section>
    <h2>Screenshots</h2>
    <p class="small">Replace these image paths with your real screenshots (stored in <code>/assets/screenshots/</code>).</p>
    <div class="grid">
      <img src="assets/screenshots/arena_overview.png" alt="Arena overview" class="sshot" />
      <img src="assets/screenshots/agent_debug.png" alt="Agent debug overlay" class="sshot" />
    </div>
  </section>

  <section>
    <h2>Contributing</h2>
    <p class="small">Contributions welcome! Please open issues for bug reports or feature requests. If you'd like to contribute code, fork the repo, create a feature branch and open a pull request describing the change and the motivation.</p>
  </section>

  <section>
    <h2>License</h2>
    <p>MIT License — see <code>LICENSE</code> file for details.</p>
  </section>

  <section>
    <h2>Contact</h2>
    <p>
      Project lead: <strong>Sasika Sewmini</strong><br/>
      Index: 225532T<br/>
      (Add your email or GitHub profile link here)
    </p>
  </section>

  <footer>
    <div class="small">If you want, I can also convert this to a Markdown `README.md` or customize text/screenshots/commands for your exact repository layout — tell me which files you have and I'll adapt it.</div>
  </footer>
</body>
</html>
