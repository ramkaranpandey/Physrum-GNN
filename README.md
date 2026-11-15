
# 🧬 Physarum-GNN: Bio-Inspired Dynamic Fleet Routing

<p align="center">
  <strong>🌐 LIVE DEMO: <a href="https://ramkaranpandey.github.io/Physrum-GNN/">Visit & Run PHYSRUM-GNN</a></strong>
</p>

**A brainless, single-celled organism—*Physarum polycephalum*, commonly known as the slime mold—demonstrates a remarkable natural approach to solving dynamic network problems.**

Long before modern computing, nature was already experimenting with adaptive networks. Instead of calculating rigid routes, this organism creates a pressurized web of tubes through which nutrients flow. When a path becomes blocked or inefficient, its tubes gradually wither, while useful alternative connections strengthen.

**What if we could bring this biological intelligence into modern transportation networks?**

That's the idea behind **Physarum-GNN**.

We combine the adaptive fluid-flow and conductivity reinforcement mechanism of *Physarum polycephalum* with a **Spatial Graph Neural Network (GNN)** to explore intelligent, congestion-aware fleet routing under dynamic road conditions.

We stress-test this approach against conventional **Dijkstra shortest-path routing** on real OpenStreetMap-derived road networks of **Guwahati, Assam, India**.

### 🚀 Explore the live simulation

**[👉 CLICK HERE TO VISIT & RUN THE LIVE PHYSRUM-GNN SIMULATION](https://ramkaranpandey.github.io/Physrum-GNN/)**

Explore the road network, select start and destination points, dispatch fleets, introduce dynamic disruptions, and compare both routing strategies through an interactive simulation.

### ⚡ Two approaches. One dynamic road network.

| Dijkstra | Physarum-GNN |
|---|---|
| Classical shortest-path algorithm | Bio-inspired adaptive routing |
| Computes shortest routes | Uses conductivity, road occupancy and GNN-informed edge scores |
| Reacts to blocked routes through rerouting | Adapts routes using retained conductivity and changing road conditions |
| Efficient for conventional shortest-path problems | Explores adaptive routing under changing network conditions |

**There is no predetermined winner.**

Dijkstra can outperform Physarum-GNN in stable networks and scenarios where computational efficiency and shortest-path optimality are the priority. Physarum-GNN can offer advantages in certain dynamic, congestion-aware scenarios where adaptive network behaviour is valuable.

The winner depends on the scenario, network conditions and evaluation metric. Our objective is not to prove that one algorithm always beats the other, but to investigate where each approach performs best under identical simulation conditions.

### 🔬 What makes this project interesting?

- **Bio-inspired computing:** Translating biological fluid-flow behaviour into a computational routing mechanism.
- **Graph Neural Networks:** Integrating spatial graph learning with adaptive conductivity-based routing.
- **Dynamic road networks:** Simulating road blockages, congestion, capacity constraints and alternative routes.
- **Real-world geographical data:** Using OpenStreetMap-derived road infrastructure from Guwahati, Assam.
- **Comparative evaluation:** Testing both algorithms under the same fleet sizes, road conditions, congestion model and disruption events.

**The central question:** Can principles found in a simple biological organism help us develop more adaptive transportation and network-routing systems?

## Fleet dashboard

### The map

The road close-up now covers about **1.65× the original connected extract**, displaying 768 mapped intersections and 875 visible links. The connected routable area has 518 selectable intersections and 667 links. The 140 purple dashed short joins are synthetic simulation roads, not verified real streets. The animated Physarum and Dijkstra maps fill the available page width and appear one after the other beneath the selection map. All three road maps retain the original pale map background, light road lines, white intersection dots, and readable map labels in either theme. The dashboard opens in a black theme; the theme toggle switches the surrounding interface to light mode if desired.

### Running a comparison

1. **Choose how many start → end paths to simulate** (1 to 10) with the *Number of start → end paths* box. Each path gets its own row in the sidebar.
2. **Set a start and an end for every path**, either from that row's two node menus or by clicking intersections on the map. Map clicks fill START 1, END 1, START 2, END 2 … in order; press **Pick on map** beside any slot to choose which one the next click sets. On the map, a filled pin is a start and a ringed pin is an end, with one colour per path. A start and end of the same path must differ and be connected by a directed route.
3. **Set the fleet size.** The default is **50 vehicles per fleet**. Enter a whole number from 1 to 2500 in the number box, or use the synchronized slider. The fleet is the total per policy and must be at least the number of paths.
4. Press **Dispatch both fleets**.

Vehicles are assigned to paths in turn (vehicle 1 to path 1, vehicle 2 to path 2, and so on), so every path receives an equal share, give or take one vehicle. Each policy gets the same number of vehicles per path, the same selected paths, and the same road speeds, capacities, and hazard events. A micro-disruption is only accepted if every selected path still has a bypass.

> **Note on the results table above:** those numbers were recorded with the earlier fixed layout, in which one selected start/end was paired with a derived nearby second depot and zone (four depot-zone combinations). The page now runs exactly the paths you select, so a one-path run is a different scenario and will give different numbers. Calling `Fleet(count=...)` without `pairs=` still uses the earlier layout.

The page opens with one path (the default Maligaon–Kamakhya route). Raising the path count fills new rows with deterministic, well-separated default paths, which you can change.

While the simulation runs you can watch live traffic, road closures, vehicle locations, and delivery counts, plus a separate route map and report card for each policy. The first graph below compares cumulative arrivals of all vehicles at each simulation tick; the colored dashed lines mark each median arrival tick. Under it, **Per-path timelines** display four paths in a 2×2 desktop grid. Fewer than four paths leave blank slots; ten paths produce three grids of four, with two blank slots in the last grid. Each graph shows only vehicles assigned to that path, with its own median, last-car tick and BPR delay for both policies. Median arrival tick and last-car tick appear only when every vehicle in that fleet has arrived; if the tick cap ends first, final times are unavailable and the live arrival curve still shows progress. Larger fleets take longer to finish and may hit the configured tick cap.

### Report cards

Each policy's card shows:

- Fleet deliveries and the last arrival tick (all paths combined; per-path figures are in the Per-path timelines section)
- BPR added drive time in minutes, shown separately from aggregate congestion wait ticks
- Aggregate congestion wait ticks
- Median arrival tick and last-car tick, shown once every vehicle has arrived
- Measured routing CPU milliseconds
- Route update and recalculation counts
- Roads used

Moving time and queued or waiting ticks are separate metrics. A simulation tick is a visualization clock, not a real travel-time unit.

> **Depot caveat:** the bundled connected component does not include verified ISBT or GMCH sites, nor the named GS Road, VIP Road, or Zoo Road alternatives. The two depots and two zones shown are **simulated positions on the mapped roads**, and the app does not present them as those real facilities.

---

## How the simulation works

### Shared conditions for both policies

- **Road closures.** Both policies see the same temporary closures each tick. A concurrent producer thread proposes seeded micro-disruptions from a pre-event corridor, independently of either policy's current route. A lock and condition coordinate it with the master tick loop.
- **Closure rules.** Closures last eight ticks and are accepted only where every selected start→end path still has a bypass.
- **Capacity.** Each road has a class-based capacity, and at most twice that number of vehicles may occupy it. Extra vehicles wait at the preceding intersection.
- **Congestion model.** For each admitted vehicle, travel duration follows the BPR formula below. The resulting simulated delay is rounded up to ticks. Both policies use identical congestion math. The backend retains the sum of free-flow and BPR road time across vehicles; the dashboard shows median arrival tick and the fleet-wide BPR penalty instead of that confusing aggregate drive-time sum. Vehicles also queue at full roads, and queue time is reported as wait ticks rather than conflated with drive minutes.

```text
travel time = free-flow time × (1 + 0.30 × (occupancy / capacity)^4)
```

### The two routing policies

| | Dijkstra | Physarum-GNN |
| --- | --- | --- |
| Initial routing | Shortest path per truck at dispatch | Capacity-aware route using conductivity and current occupancy |
| When it reroutes | Only when the remaining route is blocked, via a fresh search from the truck's current node | Chooses routes from current road occupancy and retained conductivity |
| Congestion handling | Reactive to blockages only; does not reroute solely because of congestion | Edge scores precomputed once per run; conductivity retained across ticks |
| Route extraction | Dijkstra | Weighted Dijkstra search internally |

Implementation notes:

- **NumPy is optional.** When installed, all conductivity values update in one vectorized operation. The standard-library fallback runs fully offline.
- The GUI does **not** run 100 pressure-solver iterations per frame.
- This is a routing *policy comparison*. It does not show that Physarum has lower algorithmic compute cost.

---

## CLI benchmark

`python main.py` blocks a simulated road on the original Maligaon–Kamakhya route and runs Dijkstra, warm-start Physarum, and Physarum-GNN on that same closure. It also runs the Jorabat and Panikhaiti scenarios.

### Outputs (in `output/`)

| File | Contents |
| --- | --- |
| `maligaon_before.svg` | Original route |
| `maligaon_after.svg` | Physarum detour |
| `maligaon_after_dijkstra.svg` | Dijkstra path |
| `maligaon_after_gnn.svg` | Physarum-GNN path |
| `*_routes.json` | Full paths and equivalent maps for each scenario |
| `benchmark.csv` | Benchmark results |
| `model_evaluation.csv` | GNN evaluation: recall of held-out bypass edges among the highest-scoring 5% of predictions |

### Block your own road

List the local road IDs along the original route:

```bash
python main.py --scenario maligaon --list-route
```

Then close one of them, which ensures the original route breaks:

```bash
python main.py --scenario maligaon --close-edge 14255
```

Other options:

- **Interactive mode:** `python main.py --scenario maligaon --interactive` lists IDs and lets you enter one or several comma-separated IDs at a prompt.
- **Multiple closures:** `--close-edge 14255,14256`
- **Other scenarios:** `--scenario jorabat` or `--scenario panikhaiti`
- **Close by location:** `--close-at 91.854,26.174` with `--scenario panikhaiti` blocks the nearest road to that longitude and latitude.

The IDs refer to segments in the bundled graph, not OSM way IDs.

**Reading the results**

- Each method reports whether its path remains valid, estimated drive minutes, rerouting milliseconds, and a route preview.
- Complete ordered road IDs are in the CSV. Complete route coordinates and map filenames are in `output/maligaon_custom_14255_routes.json` for the example above.
- Custom runs write distinct filenames (`*_before.svg`, `*_after.svg` for Physarum, `*_after_dijkstra.svg`, `*_after_gnn.svg`) and preserve the default maps.
- An unreachable destination produces an empty path and a blank estimated drive time.
- A closure off the original route can leave the fixed route valid.

### Measurement method

- The fixed pre-disaster route is computed before the closure and validated afterward. Zero rerouting time means it never reroutes.
- **Dijkstra** recomputes the shortest route with the closed road removed.
- **Physarum** starts from pre-event conductivity, solves nodal pressures, computes flux, and reinforces used edges while others decay. It then extracts a directed path.
- **Physarum-GNN** uses a lightweight one-hop GNN to modify the initial conductivity, with features and weights learned from simulated closures in separate corridors.
- Post-closure latency includes GNN inference, Physarum iterations, and path extraction. It excludes offline training and pre-event preparation.

---

## Data

`data/guwahati_roads.json` bundles **91,923 vertices** and **87,662 OSM-derived road segments**, of which 5,904 are marked one-way. Roads and geometries were extracted from bundled OpenFreeMap zoom-14 vector tiles. To rebuild the JSON from the cached tiles:

```bash
python scripts/build_tiles.py
```

## Limitations

- **Simulated, not real.** Speeds, capacities, destinations, congestion, and incident hazards are assumed for this demo. Closures are simulated, not observed events. Disasters and congestion are not live safety data.
- **Depots and zones are simulated positions**, not the real facilities named above (see the depot caveat).
- **Tile generalization.** Vector tiles can omit minor roads or misconnect junctions, and turn restrictions are unavailable.
- **Speeds** are assumed from road class, without traffic. Terrain and flood features are simulated proxies, not measured elevation or flood data.
- **Endpoint snapping** can move scenario endpoints away from the approximate corridor anchors. Check snapped coordinates in each `*_routes.json`.
- **Panikhaiti scenario** covers an eastbound approach toward Chandrapur, not Chandrapur itself.
- **Solver and one-way roads.** The pressure solver relaxes an undirected electrical network, while route extraction enforces one-way roads.
- **Not operational guidance.** This is an offline routing experiment and must not be used for emergency decisions.

---

## Development

```bash
python main.py --train                      # retrain the GNN
python -m unittest discover -s tests -v     # run tests
python -m pip install numpy                 # optional: vectorized conductivity updates
```

The project uses the **Python standard library only**; NumPy is an optional accelerator. The original single-vehicle dynamic experiment is kept in `physrum/dynamic.py` for reference.

## Credits

Road data © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright), licensed under ODbL, via [OpenFreeMap](https://openfreemap.org/) vector tiles.

---

## Deploy online (GitHub Pages + Render)

The dashboard is a static page, while the fleet API and simulation run in Python. GitHub Pages cannot run `app.py`, so deploy the Python service separately and point the static page at it. The included `render.yaml` creates a free Python web service in Render’s Singapore region.

### 1. Deploy the backend on Render

1. Push this project (including `app.py`, `physrum/`, `data/`, `requirements.txt`, `render.yaml`, and `.python-version`) to a GitHub repository.
2. In Render, choose **New + → Blueprint**, connect that repository, and deploy the `render.yaml` service. Alternatively create a Python Web Service with build command `pip install -r requirements.txt` and start command `python app.py`.
3. Wait for the service to become Live. Copy its public URL, such as `https://physrum-fleet-api.onrender.com`.
4. Open `https://YOUR-RENDER-URL/healthz`; it should return JSON with `"status":"ok"`.

### 2. Connect GitHub Pages to Render

1. In the repository's GitHub Pages source folder, keep `index.html`, `fleet.html`, and `config.js` together.
2. Edit `config.js` and set `window.PHYSRUM_API_BASE` to the exact Render URL (no trailing slash), for example:

   ```js
   window.PHYSRUM_API_BASE = 'https://physrum-fleet-api.onrender.com';
   ```

3. Commit and push. GitHub Pages will serve `index.html`; its requests for `/api/map`, `/api/start`, and `/api/state/...` will go to Render.
4. In **Settings → Pages**, publish from the branch and folder containing `index.html` (for example, `main` / `/root`). Open the GitHub Pages URL, hard-refresh, and check that the map loads before starting a fleet.

### Performance notes (Render deployment)

The deployed dashboard includes conservative performance improvements that do not change routing decisions, GNN scores, congestion equations, disruption timing, tick duration, or delivery metrics:

- Free-flow road-edge times are precomputed once and reused by Dijkstra; dynamic Physarum edge costs are still recalculated from the same conductivity and occupancy formula.
- Published simulation snapshots are read without deep-copying the full fleet state for every API poll. Each tick still runs and records the same simulation state.
- JSON API responses use low-level gzip compression when the browser advertises support, reducing map/state transfer size.
- Vehicle markers interpolate between backend snapshots using per-edge tick progress, so movement looks continuous instead of remaining pinned at an edge endpoint.
- Frontend state polling is sequential (no overlapping requests) and skips duplicate ticks, reducing unnecessary server and browser work.

A local repeat benchmark for 100 vehicles per policy completed in approximately 8.5–8.7 seconds over 190 simulation ticks on the test environment; actual Render time will vary with shared free-instance CPU and network conditions. This is a local measurement, not a performance guarantee.

### 3. Local development

Leave `config.js` as an empty string and run `python app.py`. The page uses the same-origin local API at `http://localhost:8000`.

### Notes

- Render's free web services may sleep after inactivity; the first request after sleep can take a little while.
- Simulation sessions are held in the backend process memory. Keep one Render instance/process for this demo; restarting or redeploying the service ends active simulations.
- `CORS_ALLOWED_ORIGINS` is set to `*` in the included starter Blueprint so GitHub Pages can call the API without extra setup. For a restricted production deployment, replace it with your exact GitHub Pages origin (for example `https://YOUR-USER.github.io`).
- The road graph is loaded from the bundled local data; no external map API key is required.
