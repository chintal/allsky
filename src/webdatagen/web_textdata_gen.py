#!/usr/bin/python

import MySQLdb
import sys
import config

def build_airtemp_file(airtemp_data, webout_temp_file, webout_humid_file):
	current_air_temp_web_data = 'Collecting data...'

	print airtemp_data

	if len(airtemp_data) >= 2:
		curr_air_temp = float(airtemp_data[0][0])
		prev_air_temp = airtemp_data[1][0]

		current_air_temp_web_data = ''

		if curr_air_temp > prev_air_temp:
			current_air_temp_web_data = "&#8593"
		elif prev_air_temp > curr_air_temp:
			current_air_temp_web_data = "&#8595"

		if curr_air_temp <= 5:
			current_air_temp_web_data += '<span class="text-info">'
		else:
			current_air_temp_web_data += '<span class="text-success">'

		current_air_temp_web_data += ' ' + str(curr_air_temp) + '</span> &#8451'

		current_air_humid_web_data = '<span class="text-info"> ' + str(airtemp_data[1][1]) \
										+ '</span>'
	else:
		current_air_humid_web_data = '<span class="text-info"> ' + str(airtemp_data[0][1]) \
										+ '</span>'

	print 'Current air temperature: ' + current_air_temp_web_data
	print 'Current air humidity: ' + current_air_humid_web_data

	with open(webout_temp_file, 'w') as web_outtemp_file:
		web_outtemp_file.write(current_air_temp_web_data)

	print 'Current air temperature stored to ' + webout_temp_file

	with open(webout_humid_file, 'w') as web_outhum_file:
		web_outhum_file.write(current_air_humid_web_data)

	print 'Current air humidity stored to ' + webout_humid_file


def build_skytemp_file(skytemp_data, airtemp_data, skytemp_file, curr_cond_file):
	current_sky_temp_web_data = 'Collecting data...'
	curr_sky_temp = 0.0
	curr_humidity = float(airtemp_data[0][1])

	if len(skytemp_data) >= 2:
		curr_sky_temp = float(skytemp_data[0][0])
		prev_sky_temp = skytemp_data[1][0]

		current_sky_temp_web_data = ''

		if curr_sky_temp > prev_sky_temp:
			current_sky_temp_web_data = "&#8593"
		else:
			current_sky_temp_web_data = "&#8595"

		current_sky_temp_web_data += ' ' + str(curr_sky_temp) + ' &#8451'

	print 'Current sky temp for web text: ' + current_sky_temp_web_data

	with open(skytemp_file, 'w') as web_skytemp_file:
		web_skytemp_file.write(current_sky_temp_web_data)

	print 'Current sky temperature stored to ' + skytemp_file

	temper_delta = float(airtemp_data[0][0]) - curr_sky_temp

	print 'Air-Sky delta = ' + str(temper_delta)

	current_cond = 'Collecting data...'

	delta_text = " (Air-Sky &#916: " + str(temper_delta) + " &#8451)"

#	if curr_humidity >= 60.0:
#		current_cond = '<span class="text-danger">worst, humidity is too high</span>'
#	else:
	if temper_delta <= 5:
		current_cond = '<span class="text-danger">worst</span>' + delta_text
	else:
		if temper_delta >= 5 and temper_delta <= 11:
			current_cond = '<span class="text-danger">very bad</span>' + delta_text
		elif temper_delta > 11 and temper_delta <= 16:
			current_cond = '<span class="text-danger">bad</span>' + delta_text
		elif temper_delta > 16 and temper_delta <= 19:
			current_cond = '<span class="text-warning">normal</span>' + delta_text
		elif temper_delta > 19 and temper_delta <= 22:
			current_cond = '<span class="text-info">quite good</span>' + delta_text
		elif temper_delta > 22 and temper_delta <= 25:
			current_cond = '<span class="text-info">good</span>' + delta_text
		elif temper_delta > 25 and temper_delta <= 35:
			current_cond = '<span class="text-success">best</span>' + delta_text
		elif temper_delta > 35:
			current_cond = '<span class="text-success">best of the best</span>' + delta_text

	print 'Current observation conditions for web: ' + current_cond

	with open(curr_cond_file, 'w') as obs_cond_file:
		obs_cond_file.write(current_cond)

	print 'Current observation conditions stored to ' + curr_cond_file


db = MySQLdb.connect(host=config.MYSQL_HOST, user=config.MYSQL_USER, \
						passwd=config.MYSQL_PASSWORD, db=config.MYSQL_DB, connect_timeout=90)

cur = db.cursor()

cur.execute("select ir_value from cloud_sensor order by time desc limit 2")

skytemp_data = cur.fetchall()

cur.execute("select temperature, humidity from external_dh22 order by time desc limit 2")

airtemp_data = cur.fetchall()

build_airtemp_file(airtemp_data, config.WEB_OUT_TEMP_FILE, config.WEB_OUT_HUMID_FILE)
build_skytemp_file(skytemp_data, airtemp_data, config.WEB_SKYTEMP_FILE, config.WEB_CURRENT_COND_FILE)

db.close()

####

db = MySQLdb.connect(host=config.MYSQL_HOST, user=config.MYSQL_USER, \
		passwd=config.MYSQL_PASSWORD, db=config.MYSQL_DB_SIMEIZ, connect_timeout=90)

cur = db.cursor()

cur.execute("select ir_value from cloud_sensor order by time desc limit 2")

skytemp_data = cur.fetchall()

cur.execute("select temperature, humidity from ambient_sensor order by time desc limit 2")

airtemp_data = cur.fetchall()

build_airtemp_file(airtemp_data, config.WEB_OUT_TEMP_SIMEIZ_FILE, config.WEB_OUT_HUMID_SIMEIZ_FILE)
build_skytemp_file(skytemp_data, airtemp_data, config.WEB_SKYTEMP_SIMEIZ_FILE, config.WEB_CURRENT_COND_SIMEIZ_FILE)

db.close()


