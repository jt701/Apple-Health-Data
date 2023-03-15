import functions as f

#record = f.xml_to_df("data/joseph_health_data/export.xml")
record = f.xml_to_df("data/josh_health_data/export.xml")
f.process_df(record)
#print(record['type'].unique())
#print(record['type'].unique())
#print(f.get_metric_df(record, "AppleStandTime"))
print(f.combined_daily_stats(record, "AppleStandTime" ))

#print(f.combined_longer_stats(record, 'StepCount'))


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