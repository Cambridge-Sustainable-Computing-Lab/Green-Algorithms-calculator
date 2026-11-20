# Green Algorithms 
**www.green-algorithms.org**

[![Generic badge](https://img.shields.io/badge/Version-v4-blue.svg)](https://shields.io/)
  
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/purple?icon=github)](https://github.com/Naereen/badges/)

---

<img src="assets/images/View_v3_classic.png" width="500">


## How to deal with the GA-data git submodule?

After cloning the repository or one of its forks, run the following to properly activate the git submodule GA-data:

```
git submodule init
git submodule update
```

We recommand running the following to add submodule information in the output of the regular `git status` command:

```
git config status.submodulesummary 1
```

When running `git pull`, git automatically fetches from the submodules but does not **update** them, meaning that you can see new commits from the submodule, they are checked-out but not included in the current repo tracked changes. To do so run:

```
git submodule update --remote
```

**Do not** apply changes to the git submodule from the current repository. Data is directly updated from the GA-data repository. For a more detailed description of the contributions recommendations, please have a look at the **online documentation**.

## Methods and data

The methodology behind the Green Algorithms project is described in our publication:
https://onlinelibrary.wiley.com/doi/10.1002/advs.202100707

All the data used for the calculator are in the `/data` directory above. 

## Questions, issues, suggestions? Want to contribute?

Start by opening an issue here, and we will try to address it quickly:
https://github.com/GreenAlgorithms/green-algorithms-tool/issues

You can also contact us at: green.algorithms@gmail.com

## How to cite this work
> Lannelongue, L., Grealey, J., Inouye, M., 
> Green Algorithms: Quantifying the Carbon Footprint of Computation. 
> Adv. Sci. 2021, 2100707. https://doi.org/10.1002/advs.202100707

## FAQ
[![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://GitHub.com/Naereen/ama)


> Should I include the number of processors, number of cores, or number of threads used?

For CPUs, the number of cores (CPUs usually have 4-12 cores per processor). For GPUs, the number of GPUs. 
If using multi-threading on CPUs (i.e. using more threads than cores), still input the number of cores, 
but be aware that your emissions might be underestimated. 

> What if my processor is not in the list? 

You can select "Other" and find the TDP (Thermal Design Power) value on the manufacturer's website. 
Plus, add a comment on [this issue](https://github.com/GreenAlgorithms/green-algorithms-tool/issues/1) so that we can add it to the list! 

> What if my country is not in the list? 

Add a comment on [this issue](https://github.com/GreenAlgorithms/green-algorithms-tool/issues/2) so that we can add it to the list!  
(some countries are more secretive than others about their energy mix). 
You can use the world average, or a close proxy, for your estimations.

> Can I compare algorithms impact independantly of the location?

Yes, simply use the "Energy needed" (in W) displayed next to the carbon emissions. 

> How do I find the usage factor of my processors?

It depends on your system. For example if you're using SLURM, `seff <job_id>` will give you the "CPU Efficiency". 
Similar commands exist for the different systems, and if you can't find it, you can just leave the default value of 1. 

> How do I estimate my Multiplicative Factor?

Try to estimate how many times you need to run your full analysis to get results you're happy with. 
It can be trials and errors, parameters optimisations, memory issues etc. 

> What if I found a bug in the tool?

[Open an issue](https://github.com/GreenAlgorithms/green-algorithms-tool/issues) on the GitHub so that we can look at it. 

## Credits 

The Green Algorithms project is led by [Dr Loïc Lannelongue](https://www.lannelongue-group.org) 
with the support of [Prof Michael Inouye](https://www.inouyelab.org/) from the University of Cambridge (UK).

### Other contributors

- [Dr Jason Grealey](https://scholar.google.com/citations?user=DiAlGKAAAAAJ&hl=en) (then: Baker Heart and Diabetes Institute, Melbourne, Australia) helped to start this project.
- Even Matencio ([GitHub](https://github.com/evenmatencio), [LinkedIn](www.linkedin.com/in/evenmatencio)) (then: French Department for the Environment, Paris, France) developed the v3.0 of the calculator and in particular the AI view. 
- The app has also been improved by [ongcp97](https://www.fiverr.com/ongcp97)


### Software and images
- The app was designed using [Plotly Dash](https://plot.ly/dash/).
- The icons used are under [CC Attribution licence](https://creativecommons.org/licenses/by/4.0/) or [flaticon licence](https://www.flaticon.com/license/license.pdf)
and have been designed by 
[Laura Reen](https://icon-icons.com/icon/weather-co2-pollution/90772),
[Jeremiah](https://icon-icons.com/icon/preferences-system-power-energy/103835),
[Sergei Kokota](https://icon-icons.com/icon/tree-greenery-nature/53329),
[Baianat](https://icon-icons.com/icon/car/61086),
[RoundIcons](https://icon-icons.com/icon/plane-airplane/89770) and
[smashingstocks](https://www.flaticon.com/ru/free-icon/industry_3033285).

## Licence

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-shield]][cc-by]

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

