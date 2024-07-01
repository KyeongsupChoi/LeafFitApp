# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from .forms import WendlerForm


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(context, request))

def wendler_view(request):
    if request.method == 'POST':

        form = WendlerForm(request.POST)

        if form.is_valid():
            # Takes the input of one Rep Max and assigns it to the number variable
            number = int(request.POST['weight'])
            global global_wendler_list

            # The list of percentages from the Wendler 531 regimen
            percentage_list = [0.40, 0.50, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]

            # Initializes a dictionary for containing calculated exercise weights
            calculated_dict = {}

            # Loop for iterating over percentage list and number to propagate calculated_dict
            for num in percentage_list:

                # Multiplies One Rep Max with Percentage then Subtracts empty bar weight and Divides by two for both sides
                calc_num = (number * num - 20) / 2

                # Conditional for rounding down to the nearest 2.5 kg (smallest plate)
                if (calc_num % 2.5) < 1.25:
                    calc_num = calc_num - (calc_num % 2.5)

                # Conditional for rounding up to the nearest 2.5 kg (smallest plate)
                else:
                    calc_num = calc_num + 2.5 - (calc_num % 2.5)

                # Conditional for replacing negatives with zeros
                if calc_num < 0:
                    calc_num = 0

                # Assigning weight value to the percentage key
                calculated_dict[num] = calc_num

            # Initializes a dictionary for containing calculated exercise sets
            exercise_dict = {
                'Week 1': {'Set 1': str(calculated_dict[0.4]) + 'kgx5',
                          'Set 2': str(calculated_dict[0.65]) + 'kgx5',
                          'Set 3': str(calculated_dict[0.75]) + 'kgx5',
                          'Set 4': str(calculated_dict[0.85]) + 'kgx5'},

                'Week 2': {'Set 1': str(calculated_dict[0.4]) + 'kgx3',
                          'Set 2': str(calculated_dict[0.7]) + 'kgx3',
                          'Set 3': str(calculated_dict[0.8]) + 'kgx3',
                          'Set 4': str(calculated_dict[0.9]) + 'kgx3'},

                'Week 3': {'Set 1': str(calculated_dict[0.4]) + 'kgx5',
                          'Set 2': str(calculated_dict[0.75]) + 'kgx5',
                          'Set 3': str(calculated_dict[0.85]) + 'kgx3',
                          'Set 4': str(calculated_dict[0.95]) + 'kgx1'},

                'Week 4': {'Set 1': str(calculated_dict[0.4]) + 'kgx5',
                          'Set 2': str(calculated_dict[0.4]) + 'kgx5',
                          'Set 3': str(calculated_dict[0.5]) + 'kgx5',
                          'Set 4': str(calculated_dict[0.6]) + 'kgx5'},
            }

            print("Woop")

            global_wendler_list = exercise_dict

            return render(request, 'home/wendler.html',
                          {'form': form, 'number': number, 'calculated_dict': exercise_dict})

    else:
        form = WendlerForm()

    return render(request, 'home/wendler.html', {'form': form})


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
