"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


openTimes = {0:[200,34], 1:[300, 32], 2:[400,32], 3:[600,30], 4:[1000,28]}
closeTimes = {0:[200,15], 1:[300,15], 2:[400,15], 3:[600,15], 4:[1000,11.428]}

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    if(control_dist_km == 0):
      return brevet_start_time

    if(control_dist_km > brevet_dist_km):
      control_dist_km = brevet_dist_km

    time = arrow.get(brevet_start_time)

    totalTime = 0
    currDist = 0
    i=0

    while(True):
      if(control_dist_km >=  openTimes[i][0]):
        totalTime += (openTimes[i][0]-currDist)/openTimes[i][1]
        currDist = openTimes[i][0]
        if(control_dist_km == openTimes[i][0]):
          break
        i+=1
      else:
        control_dist_km -= currDist
        totalTime += (control_dist_km)/openTimes[i][1]
        break

    hours = int(totalTime)
    minutes = round((totalTime - hours)*60)
    time = time.replace(hours =+ hours, minutes =+ minutes).isoformat()
    return time

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    time = arrow.get(brevet_start_time)
    if(control_dist_km == 0):
      time = time.replace(hours =+ 1).isoformat()
      return time

    if(control_dist_km > brevet_dist_km):
      control_dist_km = brevet_dist_km

    totalTime = 0
    currDist = 0
    i=0

    while(True):
      if(control_dist_km >=  closeTimes[i][0]):
        totalTime += (closeTimes[i][0]-currDist)/closeTimes[i][1]
        currDist = closeTimes[i][0]
        if(control_dist_km == closeTimes[i][0]):
          break
        i+=1
      else:
        control_dist_km -= currDist
        totalTime += (control_dist_km)/closeTimes[i][1]
        break

    hours = int(totalTime)
    minutes = round((totalTime - hours)*60)
    time = time.replace(hours =+ hours, minutes =+ minutes).isoformat()
    return time