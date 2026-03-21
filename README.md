# WMN Topology & Metric Simulator v0.1📡
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![NetworkX](https://img.shields.io/badge/networkx-3.0+-green.svg)
![NumPy](https://img.shields.io/badge/numpy-1.23+-yellow.svg)

## Overview
A Python-based software and mathematical simulator for Wireless Mesh Networks (WMN). This project demonstrates the critical difference in routing efficiency when utilizing the classic **Hop Count** metric versus the radio-oriented **Airtime Link Metric (ALM)**, as standardized in IEEE 802.11s. It uses mathematical modeling of the transmission medium to assess throughput degradation without requiring physical hardware deployment.

## The Problem
In multi-node wireless environments, directly using the Hop Count metric leads to severely sub-optimal network performance. Algorithms that minimize the number of hops naturally tend to select the longest physical links to cover maximum distance per step. 

However, at the edge of a radio transmitter's physical range, the Signal-to-Noise Ratio (SNR) drops critically. This leads to a decreased modulation rate, high Bit Error Rates (BER), and constant frame retransmissions. As a result, the route with the fewest nodes (hops) often yields the worst throughput and unpredictable latency.

## Mathematical Model
To solve this, IEEE 802.11s introduced the Airtime Link Metric (ALM), which evaluates the amount of radio "airtime" required to transmit a test frame.

The simulator algorithmically calculates the weight of each graph edge using the formula:

$$c_{a} = \left[ O + \frac{B_t}{r} \right] \times \frac{1}{1 - e_f}$$

Where:
- **$O$**: Overhead constants of PHY and MAC layers.
- **$B_t$**: Test frame size (base: 8192 bits).
- **$r$**: Physical bitrate in Mbps (modeled based on the distance between nodes).
- **$e_f$**: Frame Error Rate (FER), factoring in distance-based signal loss and normally distributed noise.

<img width="2385" height="1971" alt="wmn_simulation_result" src="https://github.com/user-attachments/assets/b2663184-6aab-4e74-9d97-5092bb05c9ac" />



## Architecture
The simulator is highly modular and structured into 4 core components:
1. **Topology Engine (`core/topology_engine.py`)**: Generates 2D coordinates for a specified number of nodes and computes Euclidean distances.
2. **RF Simulator (`core/rf_simulator.py`)**: Assigns physical bitrates and calculates FER for potential links based on physical distance, injecting Gaussian noise to simulate real-world interference.
3. **Routing Engine (`core/routing_engine.py`)**: Calculates shortest paths using Dijkstra's algorithm twice: once using Hop Count and once using the computed ALM weights.
4. **Visualizer (`core/visualizer.py`)**: Renders the network graph, highlighting the distinct paths chosen by the two routing strategies.

## Installation & Usage

1. Clone the repository and navigate to the project directory.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the simulation:
   ```bash
   # Run with default parameters
   python main.py

   # Run with custom parameters
   python main.py --nodes 50 --width 200.0 --height 200.0 --seed 42
   
   # View all available options
   python main.py --help
   ```

## Results
Upon execution, the script outputs the calculated hop counts and total ALM costs for both routing strategies in the console. It also generates an image `wmn_simulation_result.png` at the root of the project.

This visualization provides clear proof of how Hop Count often selects long, low-quality links (represented as a direct dashed red line), while ALM successfully navigates through shorter, higher-quality, and more reliable links (solid green line), improving overall network stability.
