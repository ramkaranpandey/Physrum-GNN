# PHYSRUM-GNN: live Guwahati disruption simulator

**Run the offline browser dashboard (Python 3.10+):**

```bash
python app.py
```

The app prints a fresh local `http://127.0.0.1:<port>` address and opens it in your browser. Keep the terminal open; press Ctrl+C to stop. Each launch picks a free port so an earlier demo cannot serve a stale page. Internet and extra packages are not needed.

The main map is a close-up of the bundled OSM-derived Maligaon-Kamakhya road network: a connected extract with 374 road vertices and 379 directed-aware road segments. Pick a **starting intersection** and **destination** by clicking the map, or use the preselected example. Press **Start live simulation**. The browser shows vehicle positions, current route plans, simulated road closures, and a tick-by-tick comparison. You only select endpoints; the disaster engine chooses seeded random epicenters near future routes every three ticks, using a bypass-preserving closure when possible. Affected roads are removed for both methods. Results are reproducible with the default seed.

A master tick loop advances each vehicle one road per tick. A separate producer thread proposes simulated hazards and uses a lock and condition to synchronize them with the main loop. Dijkstra recomputes from its current position when a closure touches its remaining route and records each recalculation penalty. Physarum-GNN uses bundled trained one-hop edge scores to initialize conductivity once, then retains conductivity and pressure across ticks; each tick solves one warm-started pressure/flux update and extracts a legal route. **That extraction still uses a weighted shortest-path search internally**, so these results do not prove Physarum is algorithmically superior to Dijkstra. The UI reports measured cumulative compute milliseconds, recalculation or route-update counts, estimated road travel minutes, elapsed wall seconds, and ticks to arrival. The 80 ms visual tick interval is a presentation clock, not real-world travel time. Simulated incidents, assumed road-class speeds, and tile-derived connectivity are not suitable for emergency navigation.

The previous static three-scenario Guwahati benchmark and GNN held-out evaluation remain available as an optional CLI experiment.

## Optional CLI benchmark

```bash
python main.py
```

The demo blocks a simulated road on the original Maligaon-Kamakhya route and runs Dijkstra, warm-start Physarum, and Physarum-GNN on that same closure. Open `output/maligaon_before.svg` and `output/maligaon_after.svg` for the original route and Physarum detour. `output/maligaon_after_dijkstra.svg` and `output/maligaon_after_gnn.svg` show the other paths. The command also runs Jorabat and Panikhaiti scenarios, saves equivalent maps and full paths in `output/*_routes.json`, and writes `output/benchmark.csv` plus `output/model_evaluation.csv`.

## Block your own road

```bash
python main.py --scenario maligaon --list-route
python main.py --scenario maligaon --close-edge 14255
```

The first command lists local road IDs along the original route. Use one of those IDs in the second command to ensure the original route breaks. Alternatively, run `python main.py --scenario maligaon --interactive` to list IDs and enter one or several comma-separated IDs at a prompt. For multiple closures use `--close-edge 14255,14256`. The IDs refer to segments in the bundled graph, not OSM way IDs. Other choices: `--scenario jorabat`, `--scenario panikhaiti`, or `--close-at 91.854,26.174` with `--scenario panikhaiti` to block the nearest road to a longitude and latitude.

Each method reports whether its path remains valid, estimated drive minutes, rerouting milliseconds, and a route preview. Complete ordered road IDs are in the CSV, and complete route coordinates and map filenames are in `output/maligaon_custom_14255_routes.json` for the example above. Open the corresponding `*_before.svg`, `*_after.svg` (Physarum), `*_after_dijkstra.svg`, and `*_after_gnn.svg`. Custom outputs have distinct filenames and preserve the default maps. An unreachable destination produces an empty path and blank estimated drive time. A closure off the original route can leave the fixed route valid.

## Measured comparison

The fixed pre-disaster route is computed before the closure and validated afterward; zero rerouting time means it never reroutes. Dijkstra recomputes the shortest route with the road removed. Physarum uses pre-event conductivity, solves nodal pressures, computes flux and reinforces used edges while others decay; it then extracts a directed path. The lightweight one-hop GNN modifies its initial conductivity using features and weights learned from simulated closures in separate corridors. Post-closure latency includes GNN inference, Physarum iterations, and path extraction, but excludes offline training and pre-event preparation.

One run on this machine, with simulated blockade 14255:

| Method | Valid after closure | Estimated drive | Rerouting latency |
| --- | --- | ---: | ---: |
| Fixed pre-disaster | No | unavailable | 0 ms |
| Dijkstra rerun | Yes | 5.310 min | 1.072 ms |
| Physarum | Yes | 5.310 min | 5,467.157 ms |
| Physarum-GNN | Yes | 5.310 min | 5,649.875 ms |

Timings vary by machine. Dijkstra is substantially faster in this experiment; the GNN did not improve validity or drive time. The evaluation CSV reports recall of the held-out bypass edges among the highest-scoring 5% GNN predictions. The results do not support a claim that conventional shortest-path rerouting is static or inferior.

## Data and limitations

`data/guwahati_roads.json` bundles 91,923 vertices and 87,662 OSM-derived road segments, including 5,904 marked one-way. Roads and geometries were extracted from bundled OpenFreeMap zoom-14 vector tiles; `python scripts/build_tiles.py` rebuilds the JSON from the cached tiles. Tile generalization can omit minor roads or misconnect junctions, and turn restrictions are unavailable. Endpoint snapping can move the scenario endpoints away from the approximate corridor anchors; check snapped coordinates in each `*_routes.json`. The Panikhaiti experiment covers an eastbound approach toward Chandrapur, not Chandrapur itself. The pressure solver relaxes an undirected electrical network; route extraction enforces one-way roads. Road speeds are assumed from class, without traffic; terrain and flood features are simulated proxies, not measured elevation or flood data. The closures are simulated, not observed events. This is an offline routing experiment and not operational emergency guidance.

Retrain with `python main.py --train`; run tests with `python -m unittest discover -s tests -v`. Python standard library only. Road data: [OpenStreetMap contributors](https://www.openstreetmap.org/copyright), ODbL, via [OpenFreeMap](https://openfreemap.org/) vector tiles.
