path_to_files_dir=  r"E:\NOWE SERCE ŻYCIA\Menu życia\F Outdoorsy\zepp life i strava do after effects\kuby\podejscie 2 full automacja\\"
#path_to_files_dir=  r"E:\NOWE SERCE ŻYCIA\Menu życia\F Outdoorsy\zepp life i strava do after effects\moje, strava\podejscie 2 full automacja\\"

log_filename = "log.txt"
gpx_filename = "kubaORG.gpx"
#gpx_filename = "Przehyba_z_Kuba_rower.gpx"
gpx_out_file_no_duplicates = "output_gpx_2no-duplicates.gpx"
gpx_out_file_populated = "output_gpx_3no-missing-values.gpx"

output_filename_step1_csv = gpx_filename[:gpx_filename.index(".")] + "__1data-straight-from-gpx.csv" # add postfix and change extension
output_filename_step2_csv = gpx_filename[:gpx_filename.index(".")] + "__2no-duplicates.csv" 
output_filename_step3_csv = gpx_filename[:gpx_filename.index(".")] + "__3no-missing-values.csv" 
output_filename_step4_csv = gpx_filename[:gpx_filename.index(".")] + "__4with-speed.csv" 

output_filename_step5_json = gpx_filename[:gpx_filename.index(".")] + "__5"

image_filename = "speed_graphed"

tab = "    " # 4 spaces