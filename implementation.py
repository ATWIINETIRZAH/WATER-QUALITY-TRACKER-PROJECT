





import tkinter as tk
import datetime

class Sensor:
    def __init__(self, location):
        self._location = location

    @property
    def location(self):
        return self._location

    def collect_data(self):
        raise NotImplementedError("Subclasses must implement collect_data method")

class PHSensor(Sensor):
    def __init__(self, location):
        super().__init__(location)

    def collect_data(self):
        user_input = float(input(f"Enter pH data for {self.location}: "))
        return round(user_input, 2)

class TurbiditySensor(Sensor):
    def __init__(self, location):
        super().__init__(location)

    def collect_data(self):
        user_input = float(input(f"Enter turbidity data for {self.location}: "))
        return round(user_input, 2)

class DataPoint:
    def __init__(self, sensor, time, date, measurements):
        self.sensor = sensor
        self.time = time
        self.date = date
        self.measurements = measurements

class WaterQualityTracker:
    def __init__(self):
        self._data_points = []

    def add_data_point(self, data_point):
        self._data_points.append(data_point)

    def get_data_points(self):
        return self._data_points.copy()

    def calculate_average_water_quality(self, sensor_type):
        sum_of_measurements = 0
        number_of_measurements = 0
        for data_point in self._data_points:
            if isinstance(data_point.sensor, sensor_type):
                sum_of_measurements += data_point.measurements[0]
                number_of_measurements += 1

        if number_of_measurements > 0:
            average_water_quality = sum_of_measurements / number_of_measurements
        else:
            average_water_quality = None

        return average_water_quality

    def identify_low_quality_areas(self, threshold):
        low_quality_areas = []
        for data_point in self._data_points:
            if data_point.measurements[0] < threshold:
                low_quality_areas.append(data_point.sensor.location)

        return low_quality_areas

class WaterQualityApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Water Quality Tracker")

        self.water_quality_tracker = WaterQualityTracker()

        self.label = tk.Label(self.master, text="Water Quality Tracker")
        self.label.pack()

        self.add_data_button = self.create_button("Add Data Point", self.add_data_point)
        self.average_quality_button = self.create_button("Show Average pH", self.show_average_ph)
        self.low_quality_areas_button = self.create_button("Show Low Quality Areas", self.show_low_quality_areas)

        self.result_text = tk.Text(self.master, height=10, width=50)
        self.result_text.pack()

    def create_button(self, text, command):
        button = tk.Button(self.master, text=text, command=command, bg="yellow", pady=2)
        button.pack(pady=5)
        return button

    def add_data_point(self):
        location = input("Enter location: ")
        ph_sensor = PHSensor(location)
        turbidity_sensor = TurbiditySensor(location)

        ph_data_point = DataPoint(ph_sensor, datetime.datetime.now(), "2023-08-04", [ph_sensor.collect_data()])
        turbidity_data_point = DataPoint(turbidity_sensor, datetime.datetime.now(), "2023-08-04", [turbidity_sensor.collect_data()])

        self.water_quality_tracker.add_data_point(ph_data_point)
        self.water_quality_tracker.add_data_point(turbidity_data_point)

        self.visualize_data()

    def show_average_ph(self):
        average_ph = self.water_quality_tracker.calculate_average_water_quality(PHSensor)
        if average_ph is not None:
            result = f"Average pH: {average_ph:.2f}"
        else:
            result = "No data available for pH sensor."
        self.display_result(result)

    def show_low_quality_areas(self):
        low_quality_areas = self.water_quality_tracker.identify_low_quality_areas(7.0)
        if low_quality_areas:
            result = f"Low quality areas: {', '.join(low_quality_areas)}"
        else:
            result = "No low-quality areas found."
        self.display_result(result)

    def visualize_data(self):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Visualizing Data Set\n\n")
        for data_point in self.water_quality_tracker.get_data_points():
            result_text = f"Location: {data_point.sensor.location}\n"
            result_text += f"Time: {data_point.time}\n"
            result_text += f"Date: {data_point.date}\n"
            result_text += f"Measurements: {data_point.measurements}\n\n"
            self.result_text.insert(tk.END, result_text)

    def display_result(self, result):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)


def main():
    root = tk.Tk()
    app = WaterQualityApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

