'''
The translation dict containing all the app translations.
'''


TRANSLATIONS_DICT = {

    #### APP HEADER ####

    ## TOP HEADER AND NAVIGATION BAR

    "Green Algorithms calculator": {
        "en": "Green Algorithms calculator",
        "fr": "Calculateur Green Algorithms",
    },
    "Subtitle": {
        "en": "What's the carbon footprint of your computations?",
        "fr": "Quelle est l'empreinte carbone de vos calculs ?",
    },
    "Classic-view": {
        "en": "Classic view",
        "fr": "Interface classique",
    },
    "AI-view": {
        "en": "AI view",
        "fr": "Interface IA",
    },
    "Change language": {
        "en": "Change language",
        "fr": "Choix de la langue",
    },
    "Change data version": {
        "en": "Change data version",
        "fr": "Version des données",
    },
    "Version tooltip": {
        "en": "The calculator data (carbon intensities, hardware...) is regularly updated. "
        "If you want to replicate results obtained in the past, select the corresponding data version.",
        
    },

    ## NEWS SECTION

    "Some_news": {
        "en": "Some news...",
        "fr": "Quelques actualités...",
    },
    "Carbon_intensity_update": {
        "en": '''
                ⚡️
                We are now using ElectricityMap's data for carbon intensity of electricity usage!
            ''',
        
    },
    "Release_message": {
        "en": '''
                🌱 
                v3.1 out: you can now input your own carbon footprint, the underlying data is now in a different 
                [GitHub repo](https://github.com/Cambridge-Sustainable-Computing-Lab/Green-Algorithms-data/blob/main/) 
                for better reproducibility, and we're ready for multi-language support. 
                This prepares the upcoming major update to v4.0, stay tuned! 
                
                🌍
                Multi-language is enabled, we just need to add the languages! If you want to contribute, 
                you can submit a Pull Requst directly on the GitHub repository. All you have to do is to 
                edit [this file](https://github.com/Cambridge-Sustainable-Computing-Lab/Green-Algorithms-calculator/blob/master/blueprints/translation/translation_dicts.py) 
                by adding your own language's translation to each key, we'll do the rest! 
            ''',
        
    },
    "Bugs_message": {
        "en": '''
                🐞 
                It's always possible that some bugs have slipped through the net of this new release... 
                If you spot one, just let us know 
                [here](https://github.com/GreenAlgorithms/green-algorithms-tool/issues).
            ''',
        
    },
    "More on the project website": {
        "en": "More on the project website!",
        "fr": "En savoir plus sur le projet du site !",
    },

    #### HOME PAGE ####

    ### FORM

    ### Header

    "Details about your algorithm": {
        "en": "Details about your algorithm",
        "fr": "Caractéristiques de votre algorithme",
    },
    "Home_form_subtitle": {
        "en": '''
                To understand how each parameter impacts your environmental footprint, 
                check out the formula below and the [methods article](https://onlinelibrary.wiley.com/doi/10.1002/advs.202100707)
            ''',
        
    },

    ### Runtime

    "Runtime_label": {
        "en": "Runtime (HH:MM)",
        
    },

    ### Cores

    "Type_of_cores_label": {
        "en": "Type of cores",
        
    },
    "Type_of_cores_tooltip": {
        "en": "Select the type of hardware used.",
        
    },

    # CPUs

    "Number_of_cores_used_CPU": {
        "en": "Number of cores used",
        
    },
    "CPU_number_used_tooltip": {
        "en": "Refers to the number of cores used (a single CPU contains several cores).",
        
    },
    "CPU_Model": {
        "en": "Model",
        "fr": "Modèle",
    },
    "cpu_model_tooltip": {
        "en": '''
                Select 'Average' to run the calculator with the average CPU specs. If you want to enter custom  
                CPU characteristics, please select 'I can't find my CPU' at the top of the list.
            ''',
        
    },
    "custom_cpu_title": {
        "en": '''
                If your CPU is not in the list, you can manually input the few key specs used by the calculator. 
                Pre-filled values are average ones.
            ''',
        
    },
    "Number_of_cores": {
        "en": "Number of cores",
        
    },
    "Number_of_cores_tooltip": {
        "en": "Refers to the number of cores of the CPU model. It is not the number of cores used.",
        
    },
    "CPU_TDP_(in_Watt)": {
        "en": "TDP (in Watt)",
        
    },
    "CPU_TDP_tooltip": {
        "en": "The TDP is the Thermal Design Power (TDP) of your CPU, in Watt. It is not a 'per core' value.",
        
    },
    "CPU_Die_area_(in_cm2)": {
        "en": "Die area (in cm2)",
        
    },
    "CPU_die_area_tooltip": {
        "en": "The die area of your CPU is expected in cm2. Should include the I/O die size.",
        
    },

    # GPUs

    "Number_of_GPUs_used": {
        "en": "Number of GPUs used",
        
    },
    "Number_of_GPUs_used_tooltip": {
        "en": "Refers to the number of GPUs used (no cores here).",
        
    },
    "GPU_Model": {
        "en": "Model",
        "fr": "Modèle",
    },
    "gpu_model_tooltip": {
        "en": '''
                Select 'Average' to run the calculator with the average GPU specs. If you want to enter custom  
                GPU characteristics, please select 'I can't find my GPU' at the top of the list.
            ''',
        
    },
    "custom_gpu_title": {
        "en": '''
                If your GPU is not in the list, you can manually input the few key specs used by the calculator.
                Pre-filled values are average ones.
            ''',
        
    },
    "GPU_TDP_(in_Watt)": {
        "en": "TDP (in Watt)",
        
    },
    "GPU_TDP_tooltip": {
        "en": "The TDP is the Thermal Design Power (TDP) of your GPU, in Watt.",
        
    },
    "GPU_Die_area_(in_cm2)": {
        "en": "Die area (in cm2)",
        
    },
    "GPU_die_area_tooltip": {
        "en": "The die size of your GPU is expected in cm2.",
        
    },
    "GPU_memory_(in_GB)": {
        "en": "Memory (in GB)",
        
    },
    "Memory_gpu_tooltip": {
        "en": "The GPU memory size.",
        
    },

    ### Memory

    "Memory_available": {
        "en": "Memory available (in GB)",
        
    },
    "Memory_tooltip": {
        "en": "Refers to the total memory allocated to the task, not the memory actually used.",
        
    },

    ### Computing platform

    "Select_the_platform_used": {
        "en": "Select the platform used for the computations",
        
    },
    "Select_the_platform_tooltip": {
        "en": "This field is used to retrieve specific data centre efficiency metricsand location energy mixes.",
        
    },
    "Select_server": {
        "en": "Select server",
        
    },
    "Select_location": {
        "en": "Select location",
        
    },
    "Select_location_tooltip": {
        "en": '''
                The location section is used to retrieve the electricity mix and the associated carbon intensity.
                If you want to enter a custom value, please enter 'Use a custom carbon intensity' in the continent dropdown.
            ''',
        
    },
    "Personal laptop": {
        "en": "Personal laptop",
        
    },
    "Desktop computer": {
        "en": "Desktop computer",
        
    },
    "Local server": {
        "en": "Local server",
        
    },
    "Cloud computing": {
        "en": "Cloud computing",
        
    },

    # Custom carbon intensity

    "Custom_carbon_intensity_header": {
        "en": '''
                Enter your custom carbon intensity below in gCO2e/kWh. 
                The pre-filled value corresponds to the world average electricity mix.
            ''',
        
    },
    "Carbon_intensity_title": {
        "en": 'Carbon intensity (in gCO2e/kWh)',
        
    },
    "Carbon_intensity_tooltip": {
        "en": 'Must be in gCO2e/kWh.',
        
    },
    "Carbon_intensity_used_label": {
        "en": 'Carbon intensity : ',
        
    },
    "Carbon_intensity_source": {
        "en": 'source',
        
    },

    #### CORE USAGE (CPU and GPU)

    "CPU_usage_factor_label": {
        "en": 'Do you know the real usage factor of your CPU?',
        
    },
    "CPU_usage_factor_tooltip": {
        "en": '''
                Between 0 and 1 (default: 1). This is the usage % of the cores, 
                e.g. % of the time the cores were active. 
                This can be obtained from log files for instance.
            ''',
        
    },
    "GPU_usage_factor_label": {
        "en": 'Do you know the real usage factor of your GPU?',
        
    },
    "GPU_usage_factor_tooltip": {
        "en": '''
                Between 0 and 1 (default: 1). This is the usage % of the GPUs, 
                e.g. % of the time the GPUs were active. 
                This can be obtained from log files for instance.
            ''',
        
    },
    
    ### PUE

    "PUE_label": {
        "en": 'Do you know the Power Usage Efficiency (PUE) of your local data centre?',
        
    },
    "PUE_tooltip": {
        "en": '''
                PUE is a standardised efficiency metrics measuring the 
                energy consumption of data centre overheads (e.g. cooling).
            ''',
        
    },

    ### MULTIPLICATIVE FACTOR

    "MF_label": {
        "en": 'Do you want to use a multiplicative factor?',
        
    },
    "MF_tooltip": {
        "en": '''
                Used to multiply the final results, for example when a same task is repeated 
                multiple times.
            ''',
        
    },

    #### GRAPHS ####

    "Manufacturing_impacts_vs_usage":{
        "en": 'Manufacturing impacts VS Usage'
    },
    "Computing_cores_VS_Memory": {
        "en": 'Computing cores VS Memory',
    },
    "Location_impact_graphs_title": {
        "en": 'How the location impacts your footprint',
    },
    "Power_draw_of_different_processors": {
        "en": 'Power draw of different processors',
    },

    #### IMPORT & EXPORT ####

    "Share_your_results": {
        "en": 'Export results',
        
    },
    "Import_results": {
        "en": '''**Import results**''',
        
    },
    "drag_and_drop": {
        "en": 'Drag and drop or click to select your .csv file.',
        
    },
    "error_message_header": {
        "en": '⚠️ Error when filling values from csv ⚠️',
        
    },
    "file_extension_not_csv": {
        "en": 'The file extension is not "csv".',
        
    },
    "csv_cant_be_read": {
        "en": 'The CSV file can’t be read, so doing nothing…',
        
    },
    "fields_should_be_in_csv": {
        "en": 'The following fields should be in the csv: ',
        
    },
    "wrong_fields": {
        "en": ' There seems to be typos in the csv columns name or inconsistencies in the values of the following fields: ',
        
    },
    "overall": {
        "en": '**Overall: **',
        
    },
    "inference": {
        "en": ' **Inference: **',
        
    },
    "training": {
        "en": ' **Training: **',
        
    },
    "default_error_subtitle": {
        "en": '''
                **The valid inputs contained in the csv file are filled in the form and the wrong ones are replaced by default values. 
                See below for more details** 

                If you are trying to import a csv file from previous versions, the easiest way to fix this is to manually
                input the different values in the calculator and reexport a fresh csv. You may also be trying to import a
                csv file from the home page into the AI page, which does not work.
            ''',
        
    },
    "old_version_error_subtitle": {
        "en": '''
                **It looks like you may be trying to importing an old csv from a previous version of the calculator. 
                Because of some improvements in the tool, these old CSVs should not be imported anymore 
                (some fields are missing and have to be guessed). We have filled in what we could and replaced the rest 
                by default values, but the easiest way to fix this is to manually input the different values in the 
                calculator (you can still select an older version of the data) and reexport a fresh csv. Sorry for the 
                inconvenience! (but the new features are worth it)**
            ''',
    },

    #### METRICS ####

    "Carbon_footprint": {
        "en": "Carbon footprint",
        
    },
    "Energy_needed": {
        "en": "Energy used",
        
    },
    "Carbon_sequestration": {
        "en": "Carbon sequestration",
        
    },
    "in_a_passenger_car": {
        "en": "in a passenger car",
        
    },
    "in_a_passenger_car_tooltip": {
        "en": "Equivalent distance driven by a petrol/diesel car emitting the same amount of GHGs",
        
    },
    "flights": {
        "en": "flights",
        "fr": "vols",
    },
    "of_a_flight": {
        "en": "of a flight",
        "fr": "d'un vol",
    },
    "comparison_heading": {
        "en": "Comparisons",
    },
    "suggestion_heading":{
        "en": "Questions/Suggestions?"
    },
    "suggestions": {
        "en": "If you have any suggestions or questions about the tool, you can open an issue on Github."
    },

    #### METHODOLOGY ####

    ### Header container

    "methodology_details_1": {
        "en": '''
                🌱 More details about the methodology in the [methods paper](https://onlinelibrary.wiley.com/doi/10.1002/advs.202100707).
            ''',
        
    },
    "methodology_details_2": {
        "en": '''
                🌱 Other resources you may find interesting on this topic: 
                [the GREENER principles](https://rdcu.be/dfpLM) for environmentally sustainable computational science, 
                or this [short primer](https://www.green-algorithms.org/assets/publications/2023_Comment_NRPM.pdf) 
                discussing different options for carbon footprint estimation.
            ''',
        
    },
    "methodology_details_3": {
        "en": '''
                🌱 Using a SLURM-powered HPC server? Check out [GA4HPC](https://www.green-algorithms.org/GA4HPC/)
                and the recent [Green Algorithms Dashboard](https://www.green-algorithms.org/dashboard/), they are
                great way to visualise the carbon footprint of all your jobs at once!
            ''',
        
    },
    
    ### Formula

    "The_formula_header": {
        "en": "The formula",
        
    },
    "the_formula_detail": {
        "en": '''
                The carbon footprint is calculated by estimating the energy draw of the algorithm
                and the carbon intensity of producing this energy at a given location:

                `carbon footprint = energy needed * carbon intensity`

                Where the energy needed is: 

                `runtime * (cores power draw * usage + memory power draw) * PUE * multiplicative factor`

                The power draw of the computing cores depends on the model and number of cores, 
                while the memory power draw only depends on the size of memory _available_. 
                The usage factor corrects for the real core usage (default is 1, i.e. full usage).
                The PUE (Power Usage Effectiveness) measures how much extra energy is needed 
                to operate the data centre (cooling, lighting etc.). 
                The multiplicative factor is used to take into account multiple identical runs 
                (e.g. for testing or optimisation).

                The Carbon Intensity depends on the location and the technologies used to produce electricity.
                If you want to check out the carbon intensity in real time, and see discrepancies between countries,
                check out the [ElectricityMap website](https://app.electricitymaps.com/map).
                Also, note that __the "energy needed" indicated at the top of this page is independent of the location.__
            ''',
        
    },
    
    ### Definitions

    "About_CO2e": {
        "en": "About CO2e",
        
    },
    "about_co2_detail": {
        "en": '''
                "Carbon dioxide equivalent" (CO2e) measures 
                the global warming potential of a mixture of greenhouse gases.
                __It represents the quantity of CO2 that would have 
                the same impact on global warming__ as the mix of interest
                and is used as a standardised unit to assess 
                the environmental impact of human activities.
            ''',
        
    },
    "What_is_a_tree-month": {
        "en": "What is a tree-month?",
        
    },
    "What_is_a_tree-month_details": {
        "en": '''
                It's the amount of CO2 sequestered by a tree in a month.
                __We use it to measure how long it would take to a mature tree
                to absorb the CO2 emitted by an algorithm.__
                We use the value of 11 kg CO2/year, which is roughly 1kg CO2/month.
            ''',
        
    },


    #### APP FOOTER ####

    ### DATA AND CODE

    "Data and code": {
        "en": "Data and code",
        "fr": "Code et données",
    },
    "Data_and_code_text": {
        "en": '''
                All the data and code used to run this calculator can be found on 
                [GitHub](https://github.com/Cambridge-Sustainable-Computing-Lab/Green-Algorithms-calculator)
            ''',
        "fr": '''
                Toutes les données et le code du calculateur se trouvent sur 
                [GitHub](https://github.com/Cambridge-Sustainable-Computing-Lab/Green-Algorithms-calculator)
            ''',
    },
    
    ### SUGGESTIONS

    "Questions_suggestions": {
        "en": "Questions / Suggestions?",
        "fr": "Questions / suggestions ?",
    },
    "Questions_suggestions_text": {
        "en": '''
                If you have questions or suggestions about the tool, you can 
                [open an issue](https://github.com/Cambridge-Sustainable-Computing-Lab/Green-Algorithms-calculator/issues)
                on the Github.
            ''',
        "fr": '''
                Si vous avez des questions ou des suggestions concernant l'outil, vous pouvez 
                [ouvrir une 'issue'](https://github.com/Cambridge-Sustainable-Computing-Lab/Green-Algorithms-calculator/issues) 
                sur le Github.
            ''',
    },

    ### HOW TO CITE

    "How to cite this work": {
        "en": "How to cite this work",
        "fr": "Citer ce travail",
    },
    "How_to_cite_text": {
        "en": '''
                Lannelongue, L., Grealey, J., Inouye, M., Green Algorithms: Quantifying the Carbon Footprint of Computation. 
                Adv. Sci. 2021, 2100707 [https://doi.org/10.1002/advs.202100707](https://doi.org/10.1002/advs.202100707).
            ''',
        "fr": '''
                Lannelongue, L., Grealey, J., Inouye, M., Green Algorithms: Quantifying the Carbon Footprint of Computation. 
                Adv. Sci. 2021, 2100707 [https://doi.org/10.1002/advs.202100707](https://doi.org/10.1002/advs.202100707).
            ''',
    },

    ### ABOUT US

    "About us": {
        "en": "About us",
        "fr": "Qui nous sommes",
    },
    "About_us_text": {
        "en":  '''
                    The Green Algorithms Initiative is led by the 
                    [Cambridge Sustainable Computing Lab](https://cam-sustainablecomputing.org) at the University of 
                    Cambridge, but made possible by the contribution and support of many: [full list here](https://www.green-algorithms.org/about/).
                ''',
        
    },
    "About_us_text_2": {
        "en":  '''
                    *In particular, we are thankful for the support of the Wellcome Trust, NIHR Cambridge Biomedical Research Centre, and French 
                    Department for the Ecological Transition.*
                ''',
        "fr":  '''
                    *En particulier, nous sommes reconnaissants pour le soutien 
                    du Wellcome Trust, du NIHR Cambridge Biomedical Research Centre et celui du Ministère en charge de 
                    la transition écologique français.*
                '''
    },

    ### SHOW YOUR STRIPES

    "ShowYourStripes": {
        "en": "#ShowYourStripes",
        "fr": "#ShowYourStripes",
    },
    "ShowYourStripes_text": {
        "en": '''
                These coloured stripes in the background represent the change in world temperatures 
                from 1850 to 2018. This striking design was made by Ed Hawkins from the University of Reading. 
            ''',
        
    },
    "More_on": {
        "en": '''More on [ShowYourStripes.info](https://showyourstripes.info)''',
        
    },
    "Additional_credits": {
        "en": '''
                Additional credits for the app can be found on the 
                [GitHub](https://github.com/GreenAlgorithms/green-algorithms-tool)
            ''',
        
    },

    #### HOME PAGE ####

    "How_to_report_it?": {
        "en": 'How to report it?',
        
    },
    "Report_text_header": {
        "en": '''
                It's important to track the impact 
                of computational research on climate change in order to stimulate greener algorithms.
                For that, __we believe that the carbon footprint of a project should be reported on publications
                alongside other performance metrics__. 

                Here is a text you can include in your paper:
            ''',
        
    },
    "Report_text_reference": {
        "en": ''' \[1\] Lannelongue, L., Grealey, J., Inouye, M., Green Algorithms: Quantifying the Carbon Footprint of Computation. Adv. Sci. 2021, 2100707.''',
        "fr": ''' \[1\] Lannelongue, L., Grealey, J., Inouye, M., Green Algorithms: Quantifying the Carbon Footprint of Computation. Adv. Sci. 2021, 2100707.''',
    },
    "Report_text_footer": {
        "en": ''' _Including the version of the tool is useful to keep track of the version of the data used._''',
        
    },

    #### AI PAGE ####

    "AI_page_title": {
        "en": 'The Green Algorithms calculator, adapted for artificial intelligence',
        
    },
    "Training_form_subtitle": {
        "en": '''
                This new page is especially dedicated to AI-related computations, 
                where compute is usually divided between training and inference phases. 
                The method is the same as in the original tool, 
                it simply facilitates the reporting of AI systems' environmental impacts 
                over a fixed period of time, e.g. one year.
            ''',
        
    },

    ### REPORTING PERIOD

    "Reporting_period": {
        "en": 'Reporting period',
        
    },
    "Reporting_period_explanation": {
        "en": '''
                The reporting period is the period of time over which you want to estimate
                the environmental impacts of your AI system (training and inference).
                This is particularly relevant in the case of ongoing deployment of the system.
                Typical values might be one year or the whole estimated lifespan of your system. 

                The value is only used by the calculator when you select "continuous inference"
                to report the total energy and carbon footprint over the reporting period.
                It is nonetheless good practice to enter it to clarify the scope of your
                estimations.
            ''',
        
    },

    ### TRAINING FORM

    ### Header

    "TRAINING": {
        "en": 'TRAINING',
        
    },
    "Training_form_subtitle": {
        "en": '''
                Report your training-related computations. For more information about R&D experiments, 
                retraining or overall tips regarding your reporting, please refer to the Help tab.
            ''',
        
    },

    ### R&D trainings

    "R&D_TRAINING_header": {
        "en": 'R&D TRAINING',
        
    },
    "R&D_training_label": {
        "en": 'Do you want to add R&D compute time?',
        
    },
    "R&D_training_tooltip": {
        "en": '''
                Used to add R&D compute to the final training impact. 
                If in total you estimate your R&D training computes to represent 
                twice the compute of your final training run, input '2'. 
                If total R&D is about half of the final run, input '0.5'. 
                The resulting value will be added to your main training footprint.
            ''',
        
    },

    ### Retrainings

    "RETRAINING_header": {
        "en": 'RETRAINING',
        
    },
    "retraining_label": {
        "en": 'Do you want to add retraining compute time?',
        
    },
    "retraining_tooltip": {
        "en": 'Used if you want to account for model retraining. ',
        
    },
    "Number_of_runs_label": {
        "en": 'Number of runs',
        
    },
    "Number_of_runs_tooltip": {
        "en": 'Number of times you plan to retrain the model over the reporting period.',
        
    },
    "Running_time_label": {
        "en": 'What is the relative runtime of an average retraining run compared to the main training?',
        
    },
    "Running_time_tooltip": {
        "en": 'If retraining takes on average 10% of the runtime of the main training, input "0.1".',
        
    },

    ### INFERENCE FORM
    
    ### Header

    "INFERENCE": {
        "en": 'INFERENCE',
        
    },
    "Inference_form_subtitle": {
        "en": '''
                Report your inference-related computations. For more information about continuous inference, 
                or overall tips regarding your reporting, please refer to the Help tab..
            ''',
        
    },

    ### Continuous inference section

    "Apply_continuous_inference_scheme": {
        "en": "Apply continuous inference scheme",
        
    },
    "continuous_inference_tooltip": {
        "en": '''
                See the Help tab for more information about continuous inference. 
                If chosen, then only report the computations falling within your ‘input data time span’. 
                Scaling to the reporting period is done automatically.
            ''',
        
    },
    "Input_data_time_span": {
        "en": "Input data time span",
        
    },
    "input_data_time_span_tooltip": {
        "en": '''
                The `input data time span` is the length of time over which you are able 
                to estimate your resource usage for continuous inference.
            ''',
        
    },

    ### METHODOLOGY
    
    "ai_methodology_content": {
        "en": '''
                The training and inference forms rely on the same base formula as the one used in the main
                page calculator. 
                When appropriate, retraining and R&D impacts are then added, and continuous inference impacts 
                are scaled to the reporting period.
                More information is provided by the tooltips and the help tabs.
            ''',
        
    },
    "Training_overall_description_title": {
        "en": "Overall description",
        
    },
    "Training_overall_description_content": {
        "en": '''
                The training phase of your AI system includes different stages: R&D experiments, the final training of your model, and potential retraining runs (more details are given below).
                
                We invite you to include all these stages in this form. **Start by filling-in the form based on the main training run.
                Then use the input fields available at the bottom of the form to 
                estimate the impact of R&D training and/or retraining**.
                Some R&D use cases are illustrated in more details below. 

                This approach may not work for all cases (e.g. if retraining is done with different
                hardware) but it offers a reasonable estimate. Besides, there is always the option of rerunning the calculator separately.
            ''',
        
    },
    "Training_Definitions_and_practical_tips": {
        "en": "Definitions and practical tips",
        
    },
    "Training_Definitions_and_practical_tips_content": {
        "en": '''
                __Main/final training stage__: the computations performed to achieve the final model 
                of your AI solution. 
                It can either correspond to training from scratch a custom model 
                or fine-tuning an existing model.

                __R&D training__: the compute involved in the research and development phase before the 
                final run (e.g. hyper-parameters search).
                This is included by added R&D as a fraction of the training time, 
                e.g. enter 2 if you assume that in total R&D represents 
                double the compute resources of the final run. 
                There is no typical value for that, from a small fraction in case of 
                well defined straightforward models to hundreds in more complex models requiring 
                extensive searches. For example, when studying a 176 billon parameters LLM,
                Luccioni et al. \[1\] estimated that intermediate models training and evaluation accounted 
                for approximately 150% of their main training consumption.
                
                __Retraining__: any additional training runs performed after the deployment of your AI system.
                For consistent reporting, you are invited to take into account all retraining happening 
                over your reporting period.
            ''',
        
    },
    "Training_help_references": {
        "en": '''
                '\[1\] A. S. Luccioni, S. Viguier, and A.-L. Ligozat, '
                '“Estimating the Carbon Footprint of BLOOM, a 176B Parameter Language Model,” Journal '
                'of Machine Learning Research, vol. 24, no. 253, pp. 1–15, 2023',
            ''',
        
    },
    "Inference_overall_description_title": {
        "en": "Overall description",
        
    },
    "Inference_overall_description_content": {
        "en": '''
                This is to quantify the environmental impacts of the inference phase of your AI system.
                __We distinguish between two types of inference: block, or one-shot, inference 
                (you make predictions once and for all)  and continuous inference 
                (the model makes predictions continuously over time, e.g. a chatbot)__.

                By default, the form is in 'block inference' mode but you can activate 
                the continuous mode using the switch at the top.
            ''',
        
    },
    "Inference_Definitions_and_practical_tips": {
        "en": "Definitions and practical tips",
        
    },
    "Inference_overall_description_content": {
        "en": '''
                This is to quantify the environmental impacts of the inference phase of your AI system.
                __We distinguish between two types of inference: block, or one-shot, inference 
                (you make predictions once and for all)  and continuous inference 
                (the model makes predictions continuously over time, e.g. a chatbot)__.

                By default, the form is in 'block inference' mode but you can activate 
                the continuous mode using the switch at the top.
            ''',
        
    },
    "Inference_Definitions_and_practical_tips_content": {
        "en": '''
                __Block (one-shot) inference__: for a system where prediction is made on a one-off basis 
                (or repeated occasionally).
                It may be used to process a data set as a whole or to build one-day or one-week strategy. 
                If multiple block inferences happen over your reporting period, 
                we invite you to quantify the resource needs for one inference block 
                and then to use the multiplicative factor.
            ''',
        
    },
    "Inference_Definitions_and_practical_tips_content_2": {
        "en": '''
                __Continuous inference__: corresponds to an AI service that is requested on demand 
                by users or other software systems (e.g. chatbot). 
                This inference workload does not follow a strict scheduling, making it harder to quantify. 
                In this mode, we invite you to estimate the resource usage 
                over a period of time of your choice, the so-called "input data time span”. 
                The results are then scaled up over the total reporting period. 
                For instance, if choosing a reporting scope of 1 year and filling 
                the form in continuous inference mode with an `input data time span` of 1 month,
                then your environmental impacts correspond to the monthly results multiplied by 12.
                
                It is worth keeping in mind that __the reporting period only impacts the results
                in the 'continuous inference' situation__.
            ''',
        
    },

    ### MISCELLANEOUS

    'No': { 
        "en": 'No',
        "fr": 'Non'
    },
    'Yes': { 
        "en": 'Yes',
        "fr": 'Oui'
    },
    '': { # For empty texts
        "en": '',
        "fr": ''
    },
}