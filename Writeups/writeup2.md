What micromamba command can you use to list all created environemnts?
micromamba env list

What micromamba command can you use to list all packages installed in a specific environment?
micromamba activate bioinfo_example
micromamba list

What micromamba command can you use to remove a package?
micromamba remove package_name

What micromamba command can you use to install a package from a specific channel?
micromamba install -c channel_name package_name

What micromamba command can you use to remove an environment?
micromamba env remove -n environment_name

What are all the r-base and Bioconductor packages that were installed in the bioinfo_example environment? (Hint: You may want to use one of the commands from your answers to the above questions, and combine it with the grep command.)
