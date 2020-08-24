All pre-requisite scripts used to reproduce our results "Model-Driven-Telemetry (MDT) Data Stream Anomaly Detection in Data Centers with BGP Routing"
============

- Description.
- Model-Driven-Telemetry Dataset. 
- Bravo.
- TimeProximity vs. SignatureProximity NetCorDenStream.
- Scripts to generate plots found in the paper. 

#### Description
- **Core**: We advance [```NetCorDenstream```](https://github.umn.edu/fezeu001/NetCorDenStream) that builds and improves upon [```OutlierDenStream```](https://github.com/anrputina/OutlierDenStream-BigDama18) for real-time detection of streamed anomalous MDT data. 
We show that [```NetCorDenstream```](https://github.umn.edu/fezeu001/NetCorDenStream) achieves a 59% reduction in alarms raised when compared with [```OutlierDenStream```](https://github.com/anrputina/OutlierDenStream-BigDama18), thereby reducing the (attention) burden placed on network operators.

#### Model-Driven-Telemetry (MDT) Dataset 
- The MDT data used in this work is the open sourced [```Network Anomaly Telemetry Datasets```](https://github.com/cisco-ie/telemetry).

#### Bravo
- **What?** Bravo is a “plug & play” system for “on-the-fly” customization of metrics of interests and customization of various algorithms (readily available) used in MDT data preprocessing to produce normalized ML-ready datasets.

- **Why?** Current MDT framework deployments are standardized and designed with a central telemetry data collector 

- **Broader Impact?** Bravo is portable to other MDT vendor workflow. It can be used on networks with different vendor routers producing telemetry data. The pipeline is modularized and each (optional) modules contain a readily available “bank” of tools with a variety of techniques suitable for different MDT ML tasks.

- **Efficiency?** Bravo takes less than 3 seconds to process 100,000 point and about 33 seconds to process 1.5 million data points as shown [```here```](https://github.umn.edu/fezeu001/NetCorDenStream/blob/master/plots/pdf/13-01_Exec_Time_Bravo.pdf). Thus, it can comfortably handle high speed data streams. 

#### TimeProximity vs. SignatureProximity NetCorDenStream
- **networkCorrelation**: In the ```config.json``` file on line number  [```156 (config file)```](https://github.umn.edu/fezeu001/NetCorDenStream/blob/a1c9eb33bd5a93b89c212901770fb246b31df3c5/config.json#L156), you can choose here what NetCorDenStream benchmark to use: ```timeProximity``` or ```signProximity``` NetCorDenStream. The default is [```timeProximity```](https://github.umn.edu/fezeu001/NetCorDenStream/blob/a1c9eb33bd5a93b89c212901770fb246b31df3c5/config.json#L156).

#### Scripts to generate plots found in the paper
- **Notes**: To run all the steps of the experiments and benchmarks, run all the script. The number infront of the script names indicate the execution run order, i.e. ```01_...``` scripts should be ran before ```02_...```] scripts and so on.

- **Results shown in our paper**: To reproduce all the diagrams shown in the paper, run all the scipts with the prefix ```...plot.py```.

- **TimeProximity (<img src="https://render.githubusercontent.com/render/math?math=TP_{k, \delta}">) results**: <img src="https://render.githubusercontent.com/render/math?math=TP_{k, \delta}"> alarms for <img src="https://render.githubusercontent.com/render/math?math=k=2"> and <img src="https://render.githubusercontent.com/render/math?math=\delta = [5, 30, 55]"> seconds can be found  [```here```](https://github.umn.edu/fezeu001/NetCorDenStream/blob/master/plots/k_Constant_Delta_Changing.png)
and <img src="https://render.githubusercontent.com/render/math?math=TP_{k, \delta}"> alarms for  <img src="https://render.githubusercontent.com/render/math?math=\delta=15"> and <img src="https://render.githubusercontent.com/render/math?math=k = [1, 3, 5]"> can be found [```here```](https://github.umn.edu/fezeu001/NetCorDenStream/blob/master/plots/Delta_Constant_k_Changing.png).

#### References

- [Comming...]
