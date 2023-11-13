import panel as pn
import holoviews as hv
import pandas as pd
import numpy as np
import GLOBAL_VARS as gv
from scipy.optimize import minimize
#from cerberus import Validator

pn.extension()


class GraphApp:
    def __init__(self):
        self.index = 0  # Graph index
        self.plot_pane = pn.pane.HoloViews()

        # Available functions in the selector
        possible_functions_list = list(gv.functions_dict.keys()) + ["Custom"]
        self.select_widget = pn.widgets.Select(options=possible_functions_list,
                                               name='Function')
        self.select_widget.param.watch(self.select_function, "value")
        self.selected_option = None

        # Text widgets
        self.text_title = pn.pane.Markdown("# Optimizer Viewer", style={'font-size': '16pt'})
        self.text_hint = pn.widgets.StaticText(name='Hint', value='')
        self.text_hint.value = "Select the function."
        self.text_index = pn.widgets.StaticText(value='', visible=False)
        self.text_index.value = str(self.index)

        # Input widgets
        self.custom_input_widget = pn.widgets.TextInput(name='Custom function', visible=False)
        self.lower_limit_input_widget = pn.widgets.FloatInput(name='Lower limit', visible=False)
        self.upper_limit_input_widget = pn.widgets.FloatInput(name='Upper limit', visible=False)
        self.check_function_button = pn.widgets.Button(name="Validate", button_type="primary",
                                                       visible=False, align="center")

        # Button widgets
        self.check_function_button.on_click(self.check_function)
        self.optimize_button = pn.widgets.Button(name="Optimize", button_type="primary", visible=False)
        self.optimize_button.on_click(self.start_optimization)
        self.advance_button = pn.widgets.Button(name="Advance >", button_type="primary", visible=False)
        self.advance_button.on_click(self.advance_plot)
        self.backward_button = pn.widgets.Button(name="< Backward", button_type="primary", visible=False)
        self.backward_button.on_click(self.backward_plot)

        # Vars
        self.x = None
        self.x0 = None
        self.y = None
        self.curve = None
        self.max_index = 0
        self.lower_limit = None
        self.upper_limit = None
        self.iteration_arr = None
        self.evaluation_arr = None
        self.function_expression = None

    def read_limits(self):
        """
        Read limit input widgets and set values
        :return: None
        """
        self.lower_limit = self.lower_limit_input_widget.value
        self.upper_limit = self.upper_limit_input_widget.value

        if self.lower_limit == self.upper_limit:
            self.text_hint.value = "Limits must have different values."

    def start_optimization(self, event):
        """
        Calculate optimization
        :param event: Press Optimize button
        :return: None
        """
        seed = 42
        np.random.seed(seed)
        self.read_limits()
        self.x0 = np.random.uniform(self.lower_limit,
                                    self.upper_limit)
        self.x = np.linspace(self.lower_limit,
                             self.upper_limit,
                             1000)

        if self.selected_option == "Custom":
            self.function_expression = self.custom_input_widget.value
            self.check_function()
        else:
            self.function_expression = gv.functions_dict[self.selected_option]

        x = self.x  # eval expression needs x value
        self.y = eval(self.function_expression)

        self.curve = self.plot_function()

        # list to save each function evaluation: x value and function value
        evaluation_list = []
        iteration_list = []

        def objetive_function(x):
            """
            Function to be optimized
            :param x: float to be evaluated
            :return: float f(x)
            """
            eval_result = self.evaluate_function(x)
            evaluation_list.append(np.array([x[0], eval_result[0]]))
            return eval_result

        def iteration_call(x):
            """
            Callback funtion to save each iteration result
            :param x: result of optimization
            :return: x value and function value
            """
            function_value = self.evaluate_function(x)
            iteration_list.append(np.array([x[0], function_value[0]]))

        # apply function
        result = minimize(objetive_function, self.x0,
                          method='slsqp',
                          bounds=[(self.lower_limit, self.upper_limit)],
                          options={'disp': True},
                          callback=iteration_call)

        self.evaluation_arr = np.vstack(evaluation_list)
        self.iteration_arr = np.vstack(iteration_list)

        evaluation_df = pd.DataFrame({
            'x': self.evaluation_arr[:, 0],
            'y': self.evaluation_arr[:, 1],
            'color': "blue"
        })
        evaluation_df.iloc[-1, 2] = "red"
        self.max_index = evaluation_df.shape[0]
        self.index = evaluation_df.shape[0]

        scatter = hv.Scatter(evaluation_df).opts(color=hv.dim('color').categorize({'blue': 'blue',
                                                                                   'red': 'red'}),
                                                 title='Optimization Iteration Nº={}'.format(self.max_index))
        self.plot_pane.object = self.curve * scatter
        self.text_index.value = self.max_index
        self.text_index.visible = True
        self.backward_button.visible = True
        self.advance_button.visible = True
        self.text_hint.value = "Optimization done"

    def evaluate_function(self, x):
        """
        y = f(x)
        :param x: float
        :return: float y = f(x)
        """
        return eval(self.function_expression)

    def plot_function(self):
        """
        Holoviz plot y=f(x)
        :return: hv plot object
        """
        curve = hv.Curve((self.x, self.y)).opts(width=500, height=300)
        return curve

    def check_function(self):
        """
        Validate function str
        :return: None
        """
        x = np.array([0, 1, 2])
        try:
            eval(self.function_expression)
        except Exception as error:
            self.text_hint.value = error

    def select_function(self, event):
        """
        Set selected function
        :param event: click selection in function scroll
        :return: None
        """
        self.selected_option = event.obj.value
        self.text_hint.value = "Selected function is " + self.selected_option +\
                                 ". Now fix the limits."

        if self.selected_option == "Custom":
            self.custom_input_widget.visible = True
            self.check_function_button.visible = False
        else:
            self.custom_input_widget.visible = False
            self.check_function_button.visible = False

        self.lower_limit_input_widget.visible = True
        self.upper_limit_input_widget.visible = True
        self.optimize_button.visible = True

    def advance_plot(self, event):
        """
        Plot next point
        :param event: Click on Advance button
        :return: None
        """
        if self.index < self.max_index:
            self.index += 1
            self.text_hint.value = "Advance done"
        self.text_index.value = str(self.index)
        self.update_plot()

    def backward_plot(self, event):
        """
        Plot previous point
        :param event: Click on Backward button
        :return: None
        """
        if self.index > 0:
            self.index -= 1
            self.text_hint.value = "Backward done"
        self.text_index.value = str(self.index)
        self.update_plot()

    def update_plot(self):
        """
        Plot with new points (after advance or backward)
        :return: None
        """
        evaluation_df = pd.DataFrame({
            'x': self.evaluation_arr[:self.index, 0],
            'y': self.evaluation_arr[:self.index, 1],
            'color': "blue"
        })
        evaluation_df.iloc[-1, 2] = "red"
        scatter = hv.Scatter(evaluation_df).opts(color=hv.dim('color').categorize({'blue': 'blue',
                                                                                   'red': 'red'}),
                                                 title='Optimization Nº Iteration = {}'.format(evaluation_df.shape[0]))
        self.plot_pane.object = self.curve * scatter
        self.text_index.value = evaluation_df.shape[0]

    def view(self):
        return pn.Column(
            self.text_title,
            pn.Row(
                pn.Column(self.select_widget,
                          pn.Row(self.custom_input_widget,
                                 self.check_function_button),
                          self.lower_limit_input_widget,
                          self.upper_limit_input_widget,
                          self.optimize_button,
                          self.text_hint
                          ),
                pn.Column(self.plot_pane,
                          pn.Row(self.backward_button,
                                 self.text_index,
                                 self.advance_button)
                          ),
            )
        )


app = GraphApp()
# Abrir la aplicación en el navegador predeterminado
app.view().servable(title="Optimization Viewer")
