<img align="left" src="https://user-images.githubusercontent.com/17532220/213287034-0209aa19-f8a1-418f-a325-7472510542cb.png" width="150" height="150"/>
<br>

# AMPEL-HU-astro
<br><br>


Contributed Ampel units from HU/DESY group
==========================================

## Installing

1. [Install poetry](https://python-poetry.org/docs/#installation). If you install poetry with conda, be sure to install it in its own environment, e.g. `conda create -n poetry`.
2. `git clone https://github.com/AmpelProject/Ampel-HU-astro.git; cd Ampel-HU-astro`
3. Check your virtualenv setup with `poetry env info` (or `conda run -n poetry poetry env info` if using conda). The output should include:
   ```
   Virtualenv
   Python:         3.10.x
   ```
   If not, point poetry at an installation of Python 3.10 with (`conda run -n poetry)` `poetry env use PATH_TO_PYTHON_310`
4. (`conda run -n poetry`) `poetry install -E "ztf sncosmo extcats notebook"`
5. `cd notebooks`
6. (`conda run -n poetry`) `poetry run jupyter notebook`

This will allow a number of Demo / access / development notebooks to be run. Note that most of them
requires an access token if data is to be retrieved.

## Provided units

<!-- The following are extracted from the docstrings; do not edit by hand -->
<!-- AUTOGENERATED CONTENT, do not edit below this line -->

### T0 units (alert filters):
- [LensedTransientFilter](ampel/contrib/hu/t0/LensedTransientFilter.py)
- [PredetectionFilter](ampel/contrib/hu/t0/PredetectionFilter.py): Filter derived from the DecentFilter.
- [RandFilter](ampel/contrib/hu/t0/RandFilter.py)
- [RcfFilter](ampel/contrib/hu/t0/RcfFilter.py): Filter for the ZTF Redshift Completeness Factor program..
- [RedshiftCatalogFilter](ampel/contrib/hu/t0/RedshiftCatalogFilter.py): Filter derived from DecentFilter designed to only accept transients located close to a galaxy in a catalog, and within redshift bounds.
- [SimpleDecentFilter](ampel/contrib/hu/t0/SimpleDecentFilter.py): General-purpose filter devloped alongside DecentFilter but without use of external catalogs.
- [TransientInClusterFilter](ampel/contrib/hu/t0/TransientInClusterFilter.py): Filter derived from the DecentFilter, in addition selecting candidates with position compatible with that of nearby galaxy clusters..
- [XShooterFilter](ampel/contrib/hu/t0/XShooterFilter.py): Filter derived from the DecentFilter, in addition selecting very new transients which are visible from the South.

### T2 units (augment):
- [T2BayesianBlocks](ampel/contrib/hu/t2/T2BayesianBlocks.py): T2 unit for running a bayesian block search algorithm to highlight excess regions.
- [T2BrightSNProb](ampel/contrib/hu/t2/T2BrightSNProb.py): Derive a number of simple metrics describing the rise, peak and decline of a lc.
- [T2CatalogMatchLocal](ampel/contrib/hu/t2/T2CatalogMatchLocal.py): Cross matches the position of a transient to those of sources in a set of catalogs.
- [T2DigestRedshifts](ampel/contrib/hu/t2/T2DigestRedshifts.py): Compare potential matches from different T2 units providing redshifts.
- [T2DustEchoEval](ampel/contrib/hu/t2/T2DustEchoEval.py)
- [T2ElasticcRedshiftSampler](ampel/contrib/hu/t2/T2ElasticcRedshiftSampler.py): Parse the elasticc diaSource host information and returns a list of redshifts and weights.
- [T2ElasticcReport](ampel/contrib/hu/t2/T2ElasticcReport.py): Parse a series of T2 results from T2RunParsnip and T2XgbClassifier, and create combined classifications according to the taxonomy of https://github.com/LSSTDESC/elasticc/blob/main/taxonomy/taxonomy.ipynb.
- [T2FastDecliner](ampel/contrib/hu/t2/T2FastDecliner.py): Determine decline rate in two last obs.
- [T2GetLensSNParameters](ampel/contrib/hu/t2/T2GetLensSNParameters.py)
- [T2InfantCatalogEval](ampel/contrib/hu/t2/T2InfantCatalogEval.py): Evaluate whether a transient fulfills criteria for being a potentially infant (extragalactic) transient.
- [T2KilonovaEval](ampel/contrib/hu/t2/T2KilonovaEval.py): Evaluate whether a transient fulfills criteria for being a potential kilonova-like event.
- [T2KilonovaStats](ampel/contrib/hu/t2/T2KilonovaStats.py)
- [T2LCQuality](ampel/contrib/hu/t2/T2LCQuality.py): determine the 'quality' of the light curve by computing ratios between the number of detection and that of upper limits.
- [T2LSPhotoZTap](ampel/contrib/hu/t2/T2LSPhotoZTap.py): Query the NOIR DataLab service for photometric redshifts from the Legacy Survey.
- [T2LoadRedshift](ampel/contrib/hu/t2/T2LoadRedshift.py): Add redshifts from external .csv.
- [T2MatchBTS](ampel/contrib/hu/t2/T2MatchBTS.py): Add information from the BTS explorer page.
- [T2MultiXgbClassifier](ampel/contrib/hu/t2/T2MultiXgbClassifier.py): For a range of xgboost classifier models, find a classification.
- [T2NedSNCosmo](ampel/contrib/hu/t2/T2NedSNCosmo.py): Fits lightcurves using SNCOSMO (using SALT2 defaultwise) with redshift constrained by catalog matching results.
- [T2NedTap](ampel/contrib/hu/t2/T2NedTap.py): See also.
- [T2PS1ThumbExtCat](ampel/contrib/hu/t2/T2PS1ThumbExtCat.py): Retrieve panstarrs images at datapoint location and for each tied extcat catalog matching result.
- [T2PS1ThumbNedSNCosmo](ampel/contrib/hu/t2/T2PS1ThumbNedSNCosmo.py): This state t2 unit is tied with the state T2 unit T2NedSNCosmo.
- [T2PS1ThumbNedTap](ampel/contrib/hu/t2/T2PS1ThumbNedTap.py): This point t2 unit is tied with the point T2 unit T2NedTap.
- [T2PanStarrThumbPrint](ampel/contrib/hu/t2/T2PanStarrThumbPrint.py): Retrieve panstarrs images at datapoint location and save these as compressed svg into the returned dict.
- [T2RunParsnip](ampel/contrib/hu/t2/T2RunParsnip.py): Gathers information and runs the parsnip model and classifier.
- [T2RunPossis](ampel/contrib/hu/t2/T2RunPossis.py): Load a POSSIS kilnova model and fit to a LightCurve object as process is called.
- [T2RunSncosmo](ampel/contrib/hu/t2/T2RunSncosmo.py): Gathers information and runs Sncosmo.
- [T2RunSnoopy](ampel/contrib/hu/t2/T2RunSnoopy.py): Gathers information and runs snoopy.
- [T2RunTDE](ampel/contrib/hu/t2/T2RunTDE.py): Create a TDE model and fit to a LightCurve object as process is called.
- [T2TNSEval](ampel/contrib/hu/t2/T2TNSEval.py): Evalute whether a transient fulfills criteria for submission to TNS.
- [T2XgbClassifier](ampel/contrib/hu/t2/T2XgbClassifier.py): Load a series of xgboost classifier models (distinguished by number of detections) and return a classification.

### T3 units (react):
- [AstroColibriPublisher](ampel/contrib/hu/t3/AstroColibriPublisher.py): Publish results to AstroColibri.
- [ChannelSummaryPublisher](ampel/contrib/hu/t3/ChannelSummaryPublisher.py): Create a json file with summary statistics for the channel.
- [CostCounter](ampel/contrib/hu/t3/CostCounter.py): Derive metrics for the total cost, as parsed by the provided documents.
- [ElasticcClassPublisher](ampel/contrib/hu/t3/ElasticcClassPublisher.py): This unit is intended to submit classifications to the DESC TOM db during the ELAsTICC LSST alert simulation.
- [HealpixCorrPlotter](ampel/contrib/hu/t3/HealpixCorrPlotter.py): Compare healpix coordinate P-value with output from T2RunSncosmo..
- [HealpixTokenGenerator](ampel/contrib/hu/t3/HealpixTokenGenerator.py): Based on a URL to a Healpix map.
- [PlotLightcurveSample](ampel/contrib/hu/t3/PlotLightcurveSample.py): Unit plots results from lightcurve fitters (RunSncosmo, RunParsnip).
- [RandomMapGenerator](ampel/contrib/hu/t3/RandomMapGenerator.py): Generate smoothed circular healpix probability values around a random coordinate..
- [RapidBase](ampel/contrib/hu/t3/RapidBase.py): Trigger rapid reactions.
- [RapidLco](ampel/contrib/hu/t3/RapidLco.py): Submit LCO triggers for candidates passing criteria..
- [RapidSedm](ampel/contrib/hu/t3/RapidSedm.py): Select transients for rapid reactions.
- [ScoreSingleObject](ampel/contrib/hu/t3/ScoreSingleObject.py): Calculate score based on how early a specific SN is detected.
- [ScoreTNSObjects](ampel/contrib/hu/t3/ScoreTNSObjects.py): Calculate score based on detection time reported to TNS, if any..
- [SlackSummaryPublisher](ampel/contrib/hu/t3/SlackSummaryPublisher.py)
- [TNSTalker](ampel/contrib/hu/t3/TNSTalker.py): Get TNS name if existing, and submit selected candidates.
- [TransientInfoPrinter](ampel/contrib/hu/t3/TransientInfoPrinter.py)
- [TransientTablePublisher](ampel/contrib/hu/t3/TransientTablePublisher.py): Construct a table based on selected T2 output values.
- [TransientViewDumper](ampel/contrib/hu/t3/TransientViewDumper.py)
- [VOEventPublisher](ampel/contrib/hu/t3/VOEventPublisher.py): Unit for creating a VOEvent pased on T2output and transient LightCurve.
