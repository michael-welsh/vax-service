import flask
import logging
from mysql.connector import Error
from flask import json
from lib.dbconnection import get_db_connection
from lib.scraper import scrape



app = flask.Flask(__name__)
app.config["DEBUG"] = True

logging.basicConfig(filename='logs/covid_scrape_service.log', level=logging.WARNING)

@app.route('/api/data', methods=['GET'])
def get_data():

    try:
        with db.connect() as conn:

            rv = conn.execute( "Select * from HK_SHOTS order by DATE" ).fetchall()

            dates_arr = []
            totals_arr = []
            firsts_arr = []
            seconds_arr = []

            for result in rv:

                dates_arr.append(result[0])
                totals_arr.append(result[1])
                firsts_arr.append(result[2])
                seconds_arr.append(result[3])

    except Error as error:
        #logging.error(error)
        print(error)

    all_data = {'dates': dates_arr, 'totals': totals_arr, 'firsts': firsts_arr, 'seconds': seconds_arr}

    response = app.response_class(
        response=json.dumps(all_data),
        status=200,
        mimetype='application/json'
    )
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/api/delta', methods=['GET'])
def get_delta():

    try:
        with db.connect() as conn:

            rv = conn.execute("Select * from HK_SHOTS order by DATE").fetchall()

            previous = {'date': 0, 'total': 0, 'first': 0, 'second': 0 }

            dates_arr = []
            diff_total_arr = []
            diff_first_arr = []
            diff_second_arr = []

            # Skip the first iteration to avoid skewing the data
            x = 0

            for result in rv:

                current = {'date': result[0], 'total': result[1], 'first': result[2], 'second': result[3] }
                diff_total = current['total'] - previous['total']
                diff_first = current['first'] - previous['first']
                diff_second = current['second'] - previous['second']
                previous = current

                if x > 0:
                    dates_arr.append(result[0].strftime("%d/%m"))
                    diff_total_arr.append(diff_total)
                    diff_first_arr.append(diff_first)
                    diff_second_arr.append(diff_second)

                x += 1

    except Error as error:
        #logging.error(error)
        print(error)

    finally:
        all_data = {'dates': dates_arr, 'totals': diff_total_arr, 'firsts': diff_first_arr, 'seconds': diff_second_arr}

        response = app.response_class(
            response=json.dumps(all_data),
            status=200,
            mimetype='application/json'
        )
        response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/api/percentage', methods=['GET'])
def get_percentage():

    report = {}

    try:
        with db.connect() as conn:

            rv = conn.execute("Select * from HK_SHOTS order by DATE DESC").fetchall()

            result = rv[0]

            report_date = result[0].strftime("%d/%m/%Y")
            first_shot_total = result[2]
            second_shot_total = result[3]

            hk_population = 7550515
            first_shot_percent = "{:.2%}".format(first_shot_total / hk_population)
            second_shot_percent = "{:.2%}".format(second_shot_total / hk_population)

            report = {'date': report_date, 'first_shot_percentage': first_shot_percent, 'second_shot_percentage': second_shot_percent }


    except Error as error:
        #logging.error(error)
        print(error)

    finally:

        response = app.response_class(
            response=json.dumps(report),
            status=200,
            mimetype='application/json'
        )
        response.headers.add('Access-Control-Allow-Origin', '*')

    return response


# Since the daily shots administered can only be calculated by determining how many shots
# were administered the day before, it should be done after all scraping has finished,
# since the scraping does not necessarily happen in chronological order
@app.route('/api/correct_delta', methods=['GET'])
def correct_delta():

    try:
        with db.connect() as conn:

            rv = conn.execute("Select * from HK_SHOTS order by DATE").fetchall()

            # We need to hardcode the initial values to something close to the following day, otherwise
            # the first entries will be very high values (i.e. 420000 daily first shots)
            previous = {'total': 516100, 'first': 470000, 'second': 67000 }

            for result in rv:

                current = {'date': result[0], 'total': result[1], 'first': result[2], 'second': result[3] }
                diff_total = current['total'] - previous['total']
                diff_first = current['first'] - previous['first']
                diff_second = current['second'] - previous['second']
                previous = current

                sql = "Update HK_SHOTS set first_daily = {}, second_daily = {}, total_daily = {} where Date = '{}'".format(
                    diff_first, diff_second, diff_total, result[0])
                conn.execute(sql)

    except Error as error:
        #logging.error(error)
        print(error)

    finally:
        response = app.response_class(
            response='success',
            status=200,
            mimetype='application/json'
        )
        response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/api/averages', methods=['GET'])
def get_averages():

    report = {}

    try:
        with db.connect() as conn:

            rv = conn.execute("Select first_daily, second_daily from HK_SHOTS order by DATE DESC").fetchall()
            first_shot_7_day_agg = 0
            second_shot_7_day_agg = 0
            first_shot_agg = 0
            second_shot_agg = 0
            counter = 0

            for result in rv:
                value_first = result[0]
                value_second = result[1]

                first_shot_agg += value_first
                second_shot_agg += value_second

                if(counter < 7):
                    first_shot_7_day_agg += value_first
                    second_shot_7_day_agg += value_second

                counter += 1

            first_shot_7_day_average = first_shot_7_day_agg / 7
            second_shot_7_day_average = second_shot_7_day_agg / 7
            first_shot_total_average = first_shot_agg / counter
            second_shot_total_average = second_shot_agg / counter

            report = {'first_shot_7_day_average': round(first_shot_7_day_average),
                      'second_shot_7_day_average': round(second_shot_7_day_average),
                      'first_shot_total_average': round(first_shot_total_average),
                      'second_shot_total_average': round(second_shot_total_average)}

    except Error as error:
        logging.error(error)
    finally:

        response = app.response_class(
            response=json.dumps(report),
            status=200,
            mimetype='application/json'
        )
        response.headers.add('Access-Control-Allow-Origin', '*')

    return response




@app.route('/api/update', methods=['GET'])
def do_scrape():
    scrape()
    correct_delta()

    return 'success'



db = None

@app.before_first_request
def init_pool():
    #global db
    db = db or get_db_connection()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
