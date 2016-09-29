# Goals For SN Cosmology From Twinkles

Since it is easier (faster, smaller data) to do catalog simulations of SN light curves using the same SN model assumptions that are being used in the TWINKLES setup, we should ideally use TWINKLES to study those things that cannot be studied with catalog simulations. In essence all of this has to do with studying the processing of TWINKLES data through the DM pipeline, but it also includes the process of simulating the images. 

- Single Image DM Detection of Sources: The expected method of obtaining positions of variable objects like SN is by performing image subtraction between a template and a science image, and flagging positions where the difference is incompatible with a null hypothesis that the source flux in the science image is the same as that in the template at a 'five sigma' level. We should perform difference imaging and vary the threshold of 'five sigma' to study the position and numbers of false positives as function of SNR, and the efficiency of detection of True variables  as function of SNR. Aside from SNR, we need to vary other quantities like the type of host galaxy and position with respect to host galaxy and redshift (the angular size of the host changes for similar SNR). We need to have a map of the kind (SNR, z, distance from host center/ fluxoverEffectiveHostFlux), host type, SN type) and iterate over similar quantities we can come up with.  
- Single image DM forced photometry: We need to compare the statistics of the photometry of SN using every method available as a function of measuring conditions. The conditions may include both SN near hosts and SN far away from hosts, so that one can estimate the impact of galaxy light subtraction. 
- map TWINKLES simulation results to Catalogs: Simulated catalogs using OpSim outputs of skynoise and PSF are idealized in that they assume that operations conducted within the DM pipeline work perfectly, and the PSF models are exactly the ones assumed. While the DM pipeline will improve with time, the idealized assumptions above will never be exactly true. It would be good to use the current pipeline to study what kind of systematic deviations (eg. can we train a model combining observing conditions, and environoment, idealized photometric uncertanties and model flux with known values of realistic photometric uncertainites so that it outputs measured flux and uncertainty values which might include effects increasing the uncertainty of ?) we should apply to idealized catalog simulations to incorporate the realistic DM efficiency? What is the likely impact of improving the DM pipeline?