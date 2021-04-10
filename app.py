import flask
from pvlib import solarposition, tracking
import pandas as pd
import pvlib
from pvlib import solarposition, tracking
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from datetime import datetime
import numpy as np

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    model = RandomForestRegressor(random_state=1)
    tz = 'Asia/Dili'
    lat, lon = 27, 77

    times = pd.date_range('2021-04-10', '2021-04-11', closed='left', freq='5min',
                        tz=tz)
    solpos = solarposition.get_solarposition(times, lat, lon)
    # solpos.to_csv('output.csv')

    humara_data1 = pvlib.solarposition.get_solarposition(datetime.now(), lat, lon,
                                                        altitude=None, pressure=None, method='nrel_numpy', temperature=12)

    humara_apparentZenith1 = humara_data1.apparent_zenith

    humara_zenith1 = humara_data1.zenith

    humara_apparentElevation1 = humara_data1.apparent_elevation

    humara_elevation1 = humara_data1.elevation
    humara_azimuth1 = humara_data1.azimuth
    humara_eqnOfTime1 = humara_data1.equation_of_time

    X = solpos[['apparent_zenith', 'zenith',
                'apparent_elevation', 'azimuth', 'equation_of_time']]

    y = solpos.elevation

    train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

    model.fit(train_X, train_y)

    # humara_dayOfYear = datetime.now().timetuple().tm_yday

    # humara_eqnOfTime = pvlib.solarposition.equation_of_time_spencer71(
    #     humara_dayOfYear)

    # humara_hourangle = pvlib.solarposition.hour_angle(times, lon, humara_eqnOfTime)

    # humara_declination = pvlib.solarposition.declination_cooper69(humara_dayOfYear)

    # humara_zenith = pvlib.solarposition.solar_zenith_analytical(
    #     lat, humara_hourangle, humara_declination)

    # humara_azimuth = pvlib.solarposition.solar_azimuth_analytical(
    #     lat, humara_hourangle, humara_declination, humara_zenith)

    # print("dayofyear:", humara_dayOfYear)
    # print("eqnOfTime:", humara_eqnOfTime)
    # print("humara_hourangle:", humara_hourangle[0])
    # print("humara_declination:", humara_declination)
    # print("humara_zenith:", humara_zenith[0])
    # print("humara_azimuth:", humara_azimuth[0])


    # val_predict = model.predict(val_X)

    # #val_prediction = model.predict ([humara_zenith, humara_zenith, humara_azimuth, humara_eqnOfTime])
    # vector = np.vectorize(np.int)
    humara_data = [[humara_apparentZenith1[0], humara_zenith1[0], humara_apparentElevation1[0],
                    humara_azimuth1[0], humara_eqnOfTime1[0]]]

    # humara_data = vector(humara_data)


    # #humara_data = np.array(humara_data)

    val_prediction = model.predict(humara_data)


    return str(val_prediction[0])

app.run()