import functions_messy as f
import final_functions as p

x = p.main("Data/kelley_health_data/export.xml")
print(x)
#record = f.xml_to_df("data/joseph_health_data/export.xml")
#record, workout = f.xml_to_df("data/marmor_health_data/export_fixed.xml")
#f.process_df(record)
#f.process_workout(workout)
#print(workout)
#print(record['type'].unique())
#print(record['type'].unique())
#x = f.get_metric_df(record, "SlueepAnalysis")
#print(x is None)
#print(f.reduce(x[x['sourceName'] == 'SleepWatch'], 3))
#print(f.combined_daily_stats_workout(workout, "mins" ))

#print(f.combined_daily_stats(record, 'SleepAnalysis'))


#"HKQuantityTypeIdentifierAppleStandTime"

"""
Filtered
['HeartRate' 'OxygenSaturation' 'RespiratoryRate' 'StepCount'
 'DistanceWalkingRunning' 'BasalEnergyBurned' 'ActiveEnergyBurned'
 'FlightsClimbed' 'AppleExerciseTime' 'EnvironmentalAudioExposure'
 'HeadphoneAudioExposure' 'WalkingDoubleSupportPercentage' 'WalkingSpeed'
 'WalkingStepLength' 'WalkingAsymmetryPercentage' 'RunningStrideLength'
 'RunningVerticalOscillation' 'RunningGroundContactTime' 'RunningPower'
 'RunningSpeed' 'HeartRateVariabilitySDNN']
 
 Unfiltered 
 ['HKQuantityTypeIdentifierHeight' 'HKQuantityTypeIdentifierBodyMass'
 'HKQuantityTypeIdentifierHeartRate'
 'HKQuantityTypeIdentifierRespiratoryRate'
 'HKQuantityTypeIdentifierStepCount'
 'HKQuantityTypeIdentifierDistanceWalkingRunning'
 'HKQuantityTypeIdentifierBasalEnergyBurned'
 'HKQuantityTypeIdentifierActiveEnergyBurned'
 'HKQuantityTypeIdentifierFlightsClimbed'
 'HKQuantityTypeIdentifierAppleExerciseTime'
 'HKQuantityTypeIdentifierRestingHeartRate'
 'HKQuantityTypeIdentifierVO2Max'
 'HKQuantityTypeIdentifierWalkingHeartRateAverage'
 'HKQuantityTypeIdentifierEnvironmentalAudioExposure'
 'HKQuantityTypeIdentifierHeadphoneAudioExposure'
 'HKQuantityTypeIdentifierWalkingDoubleSupportPercentage'
 'HKQuantityTypeIdentifierSixMinuteWalkTestDistance'
 'HKQuantityTypeIdentifierAppleStandTime'
 'HKQuantityTypeIdentifierWalkingSpeed'
 'HKQuantityTypeIdentifierWalkingStepLength'
 'HKQuantityTypeIdentifierWalkingAsymmetryPercentage'
 'HKQuantityTypeIdentifierStairAscentSpeed'
 'HKQuantityTypeIdentifierStairDescentSpeed' 'HKDataTypeSleepDurationGoal'
 'HKQuantityTypeIdentifierAppleWalkingSteadiness'
 'HKCategoryTypeIdentifierSleepAnalysis'
 'HKCategoryTypeIdentifierAppleStandHour'
 'HKCategoryTypeIdentifierLowHeartRateEvent'
 'HKCategoryTypeIdentifierAudioExposureEvent'
 'HKQuantityTypeIdentifierHeartRateVariabilitySDNN']
 """