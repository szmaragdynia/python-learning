path_to_files_dir=  r"E:\NOWE SERCE ŻYCIA\Menu życia\F Outdoorsy\zepp life i strava do after effects\kuby\podejscie 2 full automacja\\"

log_filename = "log.txt"
gpx_filename = "kubaORG.gpx"

output_filename_step1_csv = gpx_filename[:gpx_filename.index(".")] + "__1data-straight-from-gpx.csv" # add postfix and change extension
output_filename_step2_csv = gpx_filename[:gpx_filename.index(".")] + "__2no-duplicates.csv" 
output_filename_step3_csv = gpx_filename[:gpx_filename.index(".")] + "__3no-missing-values.csv" 
output_filename_step4_csv = gpx_filename[:gpx_filename.index(".")] + "__4with-speed.csv" 

tab = "    " # 4 spaces