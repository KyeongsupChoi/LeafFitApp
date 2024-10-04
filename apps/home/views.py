# -*- encoding: utf-8 -*-

# Import necessary modules from Django and other libraries
import os

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from docx import settings

# Import PDF generation libraries
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet

# Import Word document generation library
from docx import Document
from docx.shared import Inches

# Import custom form
from .forms import WendlerForm
from .models import WendlerPlan
from reportlab.pdfgen import canvas
import io
from django.conf import settings

from .models import WendlerPlan

# View for the dashboard page, requires login
@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(context, request))


import csv
from django.shortcuts import render
import plotly.graph_objs as go
from plotly.offline import plot


# def plot_csv(request):


# View for the Wendler 5/3/1 calculator
def wendler_view(request):
    if request.method == 'POST':
        form = WendlerForm(request.POST)
        if form.is_valid():
            # Get the one rep max weight from the form
            number = int(request.POST['weight'])
            global global_wendler_list

            # List of percentages for the Wendler 5/3/1 program
            percentage_list = [0.40, 0.50, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]

            # Calculate weights for each percentage
            calculated_dict = {}
            for num in percentage_list:
                calc_num = (number * num - 20) / 2
                # Round to nearest 2.5 kg
                if (calc_num % 2.5) < 1.25:
                    calc_num = calc_num - (calc_num % 2.5)
                else:
                    calc_num = calc_num + 2.5 - (calc_num % 2.5)
                # Replace negative values with zero
                if calc_num < 0:
                    calc_num = 0
                calculated_dict[num] = calc_num

            # Create a dictionary with the exercise plan for each week
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

            global_wendler_list = exercise_dict

            # Save the plan to the database
            plan = WendlerPlan.objects.create(
                user=request.user,
                name=form.cleaned_data.get('name', 'Default Wendler Plan'),
                weight=number
            )
            # You can create a related model to store `exercise_dict` if needed
            # For simplicity, let's assume you serialize it as JSON
            import json
            plan.exercise_data = json.dumps(exercise_dict)
            plan.save()

            return render(request, 'home/wendler.html',
                          {'form': form, 'number': number, 'calculated_dict': exercise_dict})
    else:
        form = WendlerForm()

    return render(request, 'home/wendler.html', {'form': form})

# View to generate PDF of the Wendler plan
def some_view(request):
    # Set up PDF styles and buffer
    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    buffer = io.BytesIO()
    canv = canvas.Canvas(buffer)

    # Prepare data for the PDF table
    empty_list = []
    empty_list.append(['Week No.', 'Set 1', "Set 2", "Set 3", "Set 4"])
    # Add data for each week
    for week in range(1, 5):
        empty_list.append([f'Week {week}'] + list(global_wendler_list[f'Week {week}'].values()))

    # Create header and table for PDF
    header = Paragraph("<bold><font size=18>Wendler Exercise List</font></bold>", style)
    data = empty_list
    t = Table(data)
    # Set table styles
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))
    # Add alternating row colors
    for each in range(len(data)):
        bg_color = colors.whitesmoke if each % 2 == 0 else colors.lightgrey
        t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))

    # Draw header and table on the PDF
    aW, aH = 540, 720
    w, h = header.wrap(aW, aH)
    header.drawOn(canv, 72, 800)
    aH = aH - h
    w, h = t.wrap(aW, aH)
    t.drawOn(canv, 72, aH - h)
    canv.save()

    # Return the PDF as a file response
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='WendlerSheet.pdf')

def wendler_plan_list(request):
    wendler_plans = WendlerPlan.objects.all()  # Retrieve all WendlerPlan objects
    print("farr")
    return render(request, 'home/settings.html', {'wendler_plans': wendler_plans})

# View to generate Word document of the Wendler plan
def word_doc_view(request):
    document = Document()
    docx_title = "WendlerSheet.docx"
    # Add content to the Word document
    document.add_paragraph("Wendler Exercise List")
    for week in range(1, 5):
        document.add_paragraph(f'Week {week}' + str(global_wendler_list[f'Week {week}'])[1:-1])
    document.add_page_break()

    # Prepare document for download
    f = io.BytesIO()
    document.save(f)
    length = f.tell()
    f.seek(0)
    response = HttpResponse(
        f.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = 'attachment; filename=' + docx_title
    response['Content-Length'] = length
    return response

# View for handling other pages, requires login
@login_required(login_url="/login/")
def pages(request):

    if request.path == "/transactions.html":
        # Read CSV data
        csv_data = []
        file_path = os.path.join(settings.DATA_DIR, 'apps', 'dataset', 'benchpress.csv')
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                csv_data.append(row)

        # Prepare data for Plotly
        age = [int(row['Age']) for row in csv_data]
        categories = ['Beginner', 'Novice', 'Intermediate', 'Advanced', 'Elite']

        traces = []
        for category in categories:
            y = [int(row[category]) for row in csv_data]
            trace = go.Scatter(x=age, y=y, mode='lines+markers', name=category)
            traces.append(trace)

        # Create the Plotly figure
        layout = go.Layout(title='Performance by Age and Skill Level',
                           xaxis=dict(title='Age'),
                           yaxis=dict(title='Score'))
        fig = go.Figure(data=traces, layout=layout)

        # Convert the figure to HTML
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)

        print("woof")

        return render(request, 'home/transactions.html', context={'plot_div': plot_div})
    context = {}
    try:
        load_template = request.path.split('/')[-1]
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        # Handle 404 error
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    except:
        # Handle 500 error
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))