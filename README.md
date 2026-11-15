
# Physarum-GNN: Bio-Inspired Dynamic Fleet Routing Using Spatial Graph Neural Networks

**Live Simulation:** [https://ramkaranpandey.github.io/Physrum-GNN/](https://ramkaranpandey.github.io/Physrum-GNN/)

**Visit the live application to explore the road network, run fleet simulations, introduce dynamic disruptions, and compare the performance of two fundamentally different routing approaches.**

## 1. Project Overview

Billions of years before modern computing, a brainless, single-celled organism known as *Physarum polycephalum* (commonly called slime mold) had already developed a remarkable way of adapting to changing networks.

Despite having no brain or centralized decision-making system, Physarum can construct and maintain an interconnected network of tubes to transport nutrients. Its behaviour is governed by fluid dynamics and local feedback mechanisms. Tubes carrying greater amounts of flow tend to strengthen and expand, while less useful or inactive connections gradually weaken and disappear. When conditions change or a route becomes obstructed, the organism can adapt its network by reinforcing alternative connections.

This biological behaviour raises an interesting computational question: can the principles governing a simple living organism be translated into an adaptive routing system capable of responding to changing transportation conditions?

**Physarum-GNN** explores this idea by combining the adaptive network behaviour of *Physarum polycephalum* with a Spatial Graph Neural Network (GNN) to investigate dynamic, congestion-aware fleet routing.

Rather than treating road routing exclusively as a shortest-path problem, the project explores how biological flow adaptation and graph-based learning can be applied to transportation networks where road conditions, congestion, traffic demand, and network disruptions change over time.

## 2. Biological Inspiration and Computational Approach

The central inspiration comes from the adaptive tube networks formed by *Physarum polycephalum*. Its network does not depend on a predefined global route. Instead, connections continuously adapt according to local flow conditions.

The computational model translates this principle into a graph-based transportation environment. Roads are represented as edges, intersections as nodes, and vehicles as sources of traffic demand. Edge conductivity represents the strength of a connection and is adjusted according to the simulated flow and changing network conditions.

The model explores the interaction between biological adaptation and spatial graph learning. The Physarum-inspired mechanism provides an adaptive network perspective, while the Spatial Graph Neural Network contributes learned representations of the road network and its spatial relationships.

Together, these components form the Physarum-GNN routing approach, which is evaluated against conventional Dijkstra shortest-path routing under dynamic simulation conditions.

## 3. Comparative Routing Approaches

The project evaluates two routing approaches operating on the same underlying road network.

### Dijkstra Shortest-Path Routing

Dijkstra's algorithm is a classical graph-search algorithm that computes shortest paths using non-negative edge costs. It provides a well-established baseline for evaluating routing performance and is particularly effective when network costs are relatively stable and shortest-path optimality is the primary objective.

In dynamic environments, changes in road conditions may require routes to be recalculated so that vehicles can respond to new costs or unavailable connections.

### Physarum-GNN Routing

Physarum-GNN combines biological network adaptation with spatial graph learning. Its approach is based on the principle that useful connections should be reinforced through flow, while less useful connections should gradually lose influence.

The integration of spatial graph learning provides an additional mechanism for representing relationships within the road network. This allows the project to investigate how learned graph information and adaptive conductivity can contribute to routing decisions under changing traffic conditions.

### Why Compare Both?

Neither approach is assumed to be universally superior. Dijkstra provides a strong and computationally efficient baseline for conventional shortest-path problems, while Physarum-GNN investigates the potential advantages of adaptive routing in changing network environments.

Their relative performance depends on the network structure, congestion patterns, disruption scenarios, fleet demand, and the evaluation metric being considered. Dijkstra may perform better in some scenarios, while Physarum-GNN may offer advantages in others.

The purpose of this comparison is to identify the conditions under which each approach is more effective, rather than establish a predetermined winner.

## 4. Real-World Road Network and Simulation Environment

The approaches are evaluated using real OpenStreetMap-derived road network data from Guwahati, Assam, India.

Using geographical road infrastructure provides a more representative environment than relying exclusively on artificially generated graphs. The road network is converted into a graph structure containing intersections, road segments, and their associated spatial and network information.

The simulation environment allows fleet movement and routing behaviour to be examined under changing conditions, including:

- Road congestion and varying traffic demand.
- Road blockages and network disruptions.
- Alternative route selection and adaptive rerouting.
- Multiple vehicles operating across the same road network.
- Changing network conditions affecting route costs and connectivity.
- Comparative evaluation of Dijkstra and Physarum-GNN.

The objective is to examine how both routing approaches respond to the same transportation environment and how their behaviour changes as network conditions evolve.

## 5. Live Interactive Simulation

The project includes a browser-based application that connects the frontend dashboard to a Python backend responsible for the simulation and routing operations.

**Live application:** [Visit and run the Physarum-GNN simulation](https://ramkaranpandey.github.io/Physrum-GNN/)

Through the interactive application, users can explore the road network, configure and execute fleet simulations, observe vehicle movement, introduce disruptions, and examine the resulting routing behaviour.

The application provides a visual environment for understanding how different routing strategies respond to the same network conditions, making the comparison more accessible than examining algorithmic outputs alone.

## 6. Research Objective

The broader objective of Physarum-GNN is to investigate the intersection of bio-inspired computing, graph neural networks, and intelligent transportation systems.

By translating biological network adaptation into a computational routing framework and evaluating it against a classical shortest-path baseline, the project explores whether decentralized, flow-based adaptation can contribute to more responsive routing strategies in dynamic transportation environments.

The central research question is:

**Can the adaptive network-forming principles of a simple biological organism, when combined with spatial graph learning, provide useful alternatives to conventional shortest-path routing in dynamic and congestion-prone transportation networks?**

The answer is not assumed in advance. It must emerge from comparative evaluation, simulation results, and the conditions under which each approach operates.
## 7. Fleet Dashboard

The interactive fleet dashboard provides a visual environment for configuring routing experiments, dispatching multiple vehicles, and comparing Dijkstra and Physarum-GNN under identical network conditions. It combines the geographical road network with live vehicle movement, traffic conditions, route updates, and performance measurements.

### 7.1 Road Network Visualization

The main road visualization is based on an expanded geographical extract of the Guwahati road network.

The road close-up covers approximately **1.65 times the original connected extract**, displaying 768 mapped intersections and 875 visible links. Within this visualization, the connected routable component contains 518 selectable intersections and 667 links. An additional 140 purple dashed connections represent synthetic short joins introduced for simulation purposes; these connections should not be interpreted as verified real-world streets.

The dashboard presents three road-network visualizations:

- **Selection map:** Used to choose the starting and destination intersections for each simulated path.
- **Physarum map:** Displays the vehicle movement and routing behaviour of the Physarum-GNN fleet.
- **Dijkstra map:** Displays the corresponding vehicle movement and routing behaviour of the Dijkstra fleet.

The two simulation maps occupy the available page width and are displayed sequentially beneath the selection map. All three visualizations retain the original pale geographical background, light road lines, white intersection markers, and readable map labels in both interface themes.

The dashboard opens in dark mode by default. A theme toggle is available to switch the surrounding interface to light mode.

### 7.2 Configuring and Running a Fleet Comparison

A comparison experiment is configured by selecting one or more origin-destination paths, specifying the fleet size, and dispatching both routing policies.

**1. Configure the number of paths**

Use the *Number of start → end paths* input to select between 1 and 10 paths. Each selected path receives its own configuration row in the sidebar.

**2. Select starting and destination intersections**

Each path requires a starting intersection and a destination intersection. These can be configured through the corresponding node-selection menus or directly by clicking intersections on the geographical map.

Map selection follows the sequence START 1, END 1, START 2, END 2, and so on. Alternatively, the *Pick on map* control beside an individual selection slot allows the next map click to be assigned to a specific starting or destination point.

The map distinguishes starting intersections using filled markers and destination intersections using ringed markers. Each path is assigned a separate colour to make multiple origin-destination pairs easier to identify.

A starting point and its corresponding destination must be distinct and connected by a valid directed route.

**3. Configure fleet size**

The default configuration uses **50 vehicles per fleet**. The fleet size can be changed through the numerical input or its synchronized slider.

Valid values range from 1 to 2,500 vehicles per fleet. The selected fleet size must be at least equal to the number of configured paths so that every path can receive at least one vehicle.

**4. Dispatch both fleets**

Press **Dispatch both fleets** to begin the comparison.

Vehicles are assigned to the selected paths sequentially. Vehicle 1 is assigned to path 1, vehicle 2 to path 2, and subsequent vehicles follow the same ordering. Consequently, vehicles are distributed as evenly as possible across all selected paths, with any remainder assigned to the earlier paths.

Both routing policies receive exactly the same number of vehicles on each path and operate under identical starting conditions, selected destinations, road speeds, road capacities, and hazard events.

Micro-disruptions are accepted only when every selected origin-destination path retains an available bypass.

### 7.3 Default Configuration and Interpretation of Results

The dashboard initially loads with a single origin-destination path corresponding to the default Maligaon–Kamakhya route.

Increasing the number of paths automatically populates the additional configuration rows with deterministic, spatially separated default paths. These automatically selected paths can be modified before dispatch.

**Important distinction regarding previously recorded benchmark results:**

The results table presented earlier in this project was generated using a previous fixed configuration. That configuration paired one selected starting and destination point with a derived nearby second depot and zone, producing four depot-zone combinations.

The current dashboard no longer follows that fixed arrangement. It executes exactly the origin-destination paths selected by the user. Therefore, a simulation involving one selected path represents a different experimental scenario and should not be directly compared with results generated using the earlier four-combination configuration.

For backward compatibility, calling `Fleet(count=...)` without explicitly providing `pairs=` continues to use the earlier configuration.

### 7.4 Live Simulation and Performance Visualization

During execution, the dashboard displays the evolving state of both fleets, including vehicle positions, road traffic, temporary closures, and delivery progress.

Each routing policy has its own route visualization and performance report card. This allows the two fleets to be examined independently while retaining identical simulation conditions.

The first performance graph compares the cumulative number of vehicle arrivals at each simulation tick. Coloured dashed lines indicate the corresponding median arrival ticks for the two policies.

The subsequent **Per-path timelines** section presents individual path-level results in a 2 × 2 desktop grid. Each graph contains data only for vehicles assigned to its corresponding origin-destination path.

For each path, the timelines report:

- Median vehicle arrival tick.
- Last vehicle arrival tick.
- BPR congestion-related drive-time penalty.
- Separate arrival curves for Dijkstra and Physarum-GNN.

When fewer than four paths are selected, the unused grid positions remain blank. Configurations containing more than four paths are displayed in additional grids. For example, ten paths produce three grids, with two unused positions in the final grid.

Median arrival time and last-car time are reported only after every vehicle in the corresponding fleet has arrived. If the configured simulation tick limit is reached before completion, final arrival-time statistics remain unavailable, although the live arrival curves continue to display the progress achieved during the simulation.

Larger fleets require more simulation work and may take longer to complete. Depending on the selected fleet size and network conditions, some experiments may reach the configured tick limit before all vehicles arrive.

### 7.5 Performance Report Cards

Each routing policy has an independent report card containing the following measurements:

- **Fleet deliveries:** Total number of vehicles that successfully reach their destinations across all selected paths.
- **Last arrival tick:** Simulation tick at which the final vehicle arrives, reported only after complete fleet delivery.
- **BPR added drive time:** Additional simulated driving time attributable to congestion, expressed in minutes.
- **Aggregate congestion wait:** Total waiting time accumulated by vehicles encountering capacity-constrained roads, reported in simulation ticks.
- **Median arrival tick:** Median vehicle arrival time, available after the entire fleet completes its journey.
- **Measured routing CPU time:** CPU time attributed to routing computations, reported in milliseconds.
- **Route updates and recalculations:** Number of routing updates and recalculation operations performed during the experiment.
- **Roads used:** Road connections utilized by the corresponding fleet.

Driving time and congestion-related waiting time are treated as separate quantities. The BPR metric measures additional driving time resulting from congestion, whereas aggregate wait ticks represent time spent waiting when road capacity is exhausted.

A simulation tick represents the internal visualization and simulation clock. It should not be interpreted directly as a unit of real-world travel time.

### 7.6 Depot and Zone Representation

The bundled connected road-network component does not contain verified locations for the actual ISBT or GMCH facilities, nor does it include verified alternative road corridors corresponding to the named GS Road, VIP Road, and Zoo Road locations.

The two depots and two zones displayed by the application are therefore simulated positions placed on the mapped road network. They are used to construct reproducible routing scenarios and must not be interpreted as the actual geographical locations of those facilities.

---

## 8. Simulation Architecture and Routing Methodology

The simulation evaluates both routing policies within a shared transportation environment. Road conditions, congestion calculations, vehicle demand, and disruption events are synchronized so that differences in observed performance arise from the routing approaches rather than different environmental inputs.

### 8.1 Shared Simulation Conditions

**Road closures and disruption generation**

Both routing policies experience the same temporary road closures during each simulation tick.

A separate producer thread proposes seeded micro-disruptions using a predefined pre-event corridor. The disruption-generation process operates independently of the current route selected by either routing policy.

A synchronization mechanism based on a lock and condition variable coordinates the disruption producer with the master simulation tick loop.

**Closure duration and acceptance**

Temporary closures remain active for eight simulation ticks.

A proposed closure is accepted only when every selected origin-destination path retains at least one valid bypass. This prevents a disruption from making a configured experiment structurally impossible.

**Road capacity constraints**

Each road is assigned a capacity based on its road class. The maximum permitted occupancy is twice the assigned capacity.

When the number of vehicles attempting to occupy a road exceeds this limit, additional vehicles wait at the preceding intersection until space becomes available.

This mechanism allows the simulation to represent congestion through both increased travel duration and explicit vehicle queues.

**Congestion modelling**

Vehicle travel duration is calculated using the Bureau of Public Roads (BPR) congestion function.

For each admitted vehicle, the travel duration is determined by the road's free-flow travel time and the ratio between its current occupancy and assigned capacity.

The congestion calculation is expressed as:

```text
travel time = free-flow time × (1 + 0.30 × (occupancy / capacity)^4)
```

The resulting simulated travel duration is rounded upward to the required number of simulation ticks.

Both routing policies use identical BPR congestion calculations. The backend retains the accumulated free-flow and congestion-adjusted road travel time across vehicles. However, the dashboard separates the BPR congestion penalty from aggregate queue waiting time rather than combining them into a single potentially misleading travel-time measurement.

Consequently, vehicles experience two distinct sources of delay:

1. Additional driving duration caused by congestion on occupied roads.
2. Queueing time incurred when road capacity prevents immediate entry.

These quantities are reported independently.

### 8.2 Routing Policy Comparison

The project compares two routing policies that approach network adaptation differently.

| Routing characteristic | Dijkstra | Physarum-GNN |
|---|---|---|
| Initial routing | Computes the shortest path for each vehicle at dispatch | Selects a capacity-aware route using conductivity and current road occupancy |
| Rerouting condition | Recalculates only when the remaining route becomes blocked, starting from the vehicle's current node | Selects routes using current road occupancy and retained edge conductivity |
| Congestion response | Responds to blockages but does not reroute solely because of congestion | Incorporates occupancy and retained conductivity into route selection |
| Route extraction | Dijkstra shortest-path search | Weighted Dijkstra search over adaptive edge scores |
| Network adaptation | Reactive route recalculation | Adaptive routing through retained conductivity and changing network conditions |

The comparison is intended to examine the behaviour of a conventional shortest-path baseline against a biologically inspired adaptive routing policy.

The distinction is important: the Physarum-GNN implementation does not replace shortest-path search with a completely different path-extraction algorithm. Instead, it modifies the edge weights used during route selection through its conductivity-based mechanism and GNN-informed information. Weighted Dijkstra is then used internally to extract a directed route.

### 8.3 Implementation Details

**Optional NumPy acceleration**

NumPy is an optional dependency. When available, conductivity updates are performed through vectorized operations, allowing multiple edge values to be updated in a single operation.

When NumPy is unavailable, the implementation falls back to standard-library operations and remains capable of running offline.

**Visualization and pressure-solver separation**

The graphical interface does not execute 100 pressure-solver iterations during every visualization frame. Simulation computation and visual presentation are separated to avoid unnecessarily coupling the rendering process to the full numerical workload.

**Interpretation of computational performance**

This is a comparison of routing policies and their behaviour under shared simulation conditions. It should not be interpreted as evidence that Physarum-GNN necessarily has a lower computational cost than Dijkstra.

Routing quality, arrival performance, congestion behaviour, and computational overhead are distinct evaluation dimensions and should be interpreted separately.

---

## 9. Command-Line Benchmarking

In addition to the interactive dashboard, the project provides a command-line benchmarking environment for evaluating route selection under controlled road-network disruptions.

Running:

```bash
python main.py
```

executes the default benchmarking workflow. It blocks a road segment on the original Maligaon–Kamakhya route and evaluates three approaches under the same closure:

- Dijkstra shortest-path routing.
- Warm-start Physarum routing.
- Physarum-GNN routing.

The benchmark also executes the Jorabat and Panikhaiti scenarios, providing additional geographical and network configurations for evaluating route adaptation.

### 9.1 Benchmark Outputs

Generated files are stored in the `output/` directory.

| File | Description |
|---|---|
| `maligaon_before.svg` | Road network and original route before the disruption |
| `maligaon_after.svg` | Route selected by the Physarum approach after the disruption |
| `maligaon_after_dijkstra.svg` | Route selected by Dijkstra after the disruption |
| `maligaon_after_gnn.svg` | Route selected by Physarum-GNN after the disruption |
| `*_routes.json` | Complete route information and equivalent geographical representations for each scenario |
| `benchmark.csv` | Comparative benchmarking measurements |
| `model_evaluation.csv` | GNN evaluation results, including recall of held-out bypass edges among the highest-scoring 5% of predictions |

### 9.2 Identifying Road Segments Along a Route

To inspect the local road-segment IDs associated with the original Maligaon–Kamakhya route, run:

```bash
python main.py --scenario maligaon --list-route
```

The command displays the road IDs along the selected route.

To close a specific road segment and force the original route to become unavailable, use:

```bash
python main.py --scenario maligaon --close-edge 14255
```

The specified road ID is an example and should be replaced with an ID obtained from the route listing.

### 9.3 Additional Benchmark Options

The command-line interface supports several additional configurations.

**Interactive road selection**

```bash
python main.py --scenario maligaon --interactive
```

This mode lists the relevant road IDs and allows one or more IDs to be entered interactively as comma-separated values.

**Multiple road closures**

```bash
python main.py --scenario maligaon --close-edge 14255,14256
```

This allows multiple road segments to be blocked within the same experiment.

**Alternative geographical scenarios**

```bash
python main.py --scenario jorabat
```

```bash
python main.py --scenario panikhaiti
```

These commands execute the corresponding predefined geographical scenarios.

**Location-based road closure**

```bash
python main.py --scenario panikhaiti --close-at 91.854,26.174
```

This option blocks the road segment nearest to the specified longitude and latitude.

The road IDs used by these commands refer to segments in the bundled graph and are not OpenStreetMap way IDs.

### 9.4 Interpreting Benchmark Results

Each routing method reports whether its resulting path remains valid, its estimated driving duration, the time required for rerouting, and a route preview.

The benchmark CSV contains complete ordered road IDs for the evaluated routes. Corresponding route coordinates and generated map filenames are available in the scenario-specific JSON output.

For example, a custom Maligaon experiment closing road segment `14255` produces:

```text
output/maligaon_custom_14255_routes.json
```

Custom experiments generate distinct output files, including:

- `*_before.svg`
- `*_after.svg`
- `*_after_dijkstra.svg`
- `*_after_gnn.svg`

The default benchmark maps are preserved rather than overwritten by custom experiments.

If a destination becomes unreachable, the corresponding method returns an empty path and its estimated driving time is left blank.

A closure that does not intersect the original route may leave the original fixed route valid. In such cases, the experiment does not necessarily require rerouting.

### 9.5 Benchmark Measurement Methodology

The benchmarking process distinguishes between the original pre-disruption route and the route selected after the network changes.

**Original route**

The fixed pre-disaster route is computed before the closure is introduced and validated again afterward. If it remains valid, the original route can be retained without recalculation. A reported rerouting time of zero therefore means that no rerouting operation was required.

**Dijkstra**

After a road closure, Dijkstra computes a new shortest path with the closed road removed from the graph. The search is performed from the relevant origin to the destination under the updated network conditions.

**Physarum**

The warm-start Physarum approach begins with the conductivity state established before the disruption. It solves nodal pressures, calculates the resulting edge flux, and reinforces used connections while allowing less-used connections to decay.

A directed route is subsequently extracted from the updated network.

**Physarum-GNN**

Physarum-GNN uses a lightweight one-hop Graph Neural Network to modify the initial conductivity values.

Its features and weights are learned from simulated road closures occurring in separate corridors. The resulting GNN-informed conductivity is then used by the Physarum-based routing mechanism to evaluate the disrupted network.

**Post-disruption computational latency**

The reported post-closure latency includes GNN inference, Physarum iterations, and route extraction.

It excludes offline model training and pre-event preparation. This distinction is important when interpreting the computational measurements because the benchmark evaluates the cost of responding to a disruption rather than the total cost of developing or training the model.

---

## 10. Road Network Data

The project includes a bundled geographical road-network dataset stored at:

```text
data/guwahati_roads.json
```

The dataset contains **91,923 vertices and 87,662 OpenStreetMap-derived road segments**, of which 5,904 are marked as one-way roads.

Road geometries and network information were extracted from bundled OpenFreeMap vector tiles at zoom level 14. The resulting dataset provides the geographical and graph-based infrastructure used by the simulation and routing algorithms.

The bundled JSON file allows the project to operate using local road-network data without requiring a live external map-data request during simulation.

To rebuild the road-network JSON from the cached vector tiles, execute:

```bash
python scripts/build_tiles.py
```

The resulting dataset is used by the application to construct the road graph and support route selection, vehicle movement, congestion calculations, and disruption experiments.

---

## 11. Limitations and Modelling Assumptions

The project is a computational simulation of adaptive routing behaviour. Its results should be interpreted within the assumptions and limitations of the underlying road data, traffic model, routing algorithms, and geographical representation.

**Simulated traffic conditions**

Vehicle speeds, road capacities, destinations, congestion patterns, and incident hazards are assumed or generated for experimental purposes. Road closures represent simulated disruptions rather than verified real-world traffic incidents.

The application does not use live traffic measurements or provide real-time safety information.

**Simulated depots and zones**

The displayed depot and zone locations are simulated positions on the bundled road network. They should not be interpreted as verified locations of ISBT, GMCH, or other named facilities.

**Road-network generalization**

The geographical network is derived from vector tiles. Tile generalization may omit minor roads, simplify road geometries, or produce imperfect junction connectivity. Detailed turn restrictions are not available in the bundled representation.

**Assumed road speeds**

Road speeds are assigned using assumed road-class-based values rather than measured traffic speeds. Terrain and flood-related characteristics are represented through simulated proxies and should not be interpreted as measured elevation or observed flood conditions.

**Endpoint snapping**

Selected scenario endpoints may be snapped to nearby intersections in the bundled graph. This can cause the final simulation coordinates to differ from the approximate geographical corridor anchors. The snapped coordinates can be inspected in the corresponding `*_routes.json` files.

**Panikhaiti scenario coverage**

The Panikhaiti scenario represents an eastbound approach toward Chandrapur rather than a route terminating within Chandrapur itself.

**Pressure-solver and one-way road distinction**

The Physarum pressure solver operates on an undirected electrical-network representation. However, route extraction enforces the directionality of one-way roads. Consequently, the physical assumptions of the pressure-solving stage and the directed constraints of the final route-selection stage are not identical.

**Not intended for operational navigation**

This project is an experimental routing and simulation framework. Its outputs should not be used for emergency response, operational fleet dispatch, or real-world transportation decisions without independent validation against reliable traffic, road, and safety data.

---

The project primarily uses the **Python standard library**, with NumPy available as an optional accelerator. The original single-vehicle dynamic routing experiment is retained in `physrum/dynamic.py` for reference.

## 12. Credits and Data Attribution

The geographical road-network data used in this project is derived from OpenStreetMap contributors and distributed through OpenFreeMap vector tiles.

- Road data: [© OpenStreetMap contributors](https://www.openstreetmap.org/copyright)
- Vector tile provider: [OpenFreeMap](https://openfreemap.org/)
- OpenStreetMap data is licensed under the Open Database License (ODbL).

The project uses these geographical resources to construct a reproducible road-network environment for studying bio-inspired routing, graph-based learning, and dynamic fleet simulation.
