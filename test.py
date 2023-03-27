import functions as f

#record = f.xml_to_df("data/joseph_health_data/export.xml")
record, workout = f.xml_to_df("data/marmor_health_data/export_fixed.xml")
f.process_df(record)
f.process_workout(workout)
print(workout)
#print(record['type'].unique())
#print(record['type'].unique())
#x = f.get_metric_df(record, "SleepAnalysis")
#print(x)
#print(f.reduce(x[x['sourceName'] == 'SleepWatch'], 3))
#print(f.combined_longer_stats(record, "StepCount" ))

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