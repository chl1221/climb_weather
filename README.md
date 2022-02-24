# climb_weather
This application provides nearby climbing destinations (geographic distance) with nice weather for the coming weekend!

Defination of a valid climbing spot:
  1. Distance <= 150 miles
  2. has a nice weather on the coming weekend
      a. the highest temperature <= 82°F (27.8°C)
      b. the lowest temperature >= 65°F (18.3°C)
      c. the probability of precipitation <= 10%
      d. the wind speed <= 6

# Requirements
The application uses API from https://www.climbingweather.com (API key is not required) and https://positionstack.com (API key required [Free]).
