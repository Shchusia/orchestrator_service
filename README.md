# orch_serv
[![Coverage Status](https://img.shields.io/badge/%20Python%20Versions-%3E%3D3.10-informational)](https://pypi.org/project/orch-serv/)
[![Coverage Status](https://coveralls.io/repos/github/Shchusia/orchestrator_service/badge.svg)](https://coveralls.io/github/Shchusia/orchestrator_service)

[![Coverage Status](https://img.shields.io/badge/Version-0.2.0-informational)](https://pypi.org/project/orch-serv/)
[![Coverage Status](https://img.shields.io/badge/Docs-passed-green)](https://github.com/Shchusia/orchestrator_service/tree/master/docs)
> A library for microservice architecture, for interconnected services with different execution sequences, for orchestration services designed for such kind of services relationships.


### Installation

```bash
pip install orch_serv
```

### Problem

We have a microservice architecture

Your architecture has many services. Each individual service performs its own task. You need to set up the sequence of interactions between services, taking into account that one service can be connected to others and fired in a different sequence.

<u>Example:</u>

Task | Service execution sequence 
--- | --- 
*Task1* | service1 -> service2 -> service3
*Task2* | service2 -> service4 -> service1
*...* | ...
*TaskN* | service3 -> service2 -> ... -> serviceM

For centralized management of the services interactions, we offer an **orchestrator**: service containing valid block connections.

![file not found](http://raw.githubusercontent.com/Shchusia/orchestrator_service/refs/heads/master/materials/solution_application_diagram.png "solution_application_diagram")

What you need to do in the orchestrator service:
- create blocks with known interaction logic with the services they belong to,
- create accessible flows from these blocks (for different tasks there can be your specific flows, it is important to use unique flow names),
- define a message for the interaction of services, such that they have a single standard and override key methods,
- initialize the orchestrator and use,
- [More details](./orяch_serv/orchestrator/README.md).

What you need to use the service:
- define a message for the interaction of services, such that they have a single standard and override key methods,
- define the commands in the service which are going to be executed and what to do after the main task is completed (this is divided to separate the logic).
- [More details](./orch_serv/service/README.md)

#### Bonus

Added functionality for the formation of a sequence of steps - [details here](./orch_serv/stepper/README.MD)
