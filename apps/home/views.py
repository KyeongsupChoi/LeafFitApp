# -*- encoding: utf-8 -*-

# Import necessary Django modules and other libraries
import os
import json
import io
import csv
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.conf import settings

# Import PDF and Word document generation libraries
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from docx import Document
from docx.shared import Inches

# Import custom form and models
from .forms import WendlerForm, WendlerPlanForm
from .models import WendlerPlan

# Import Plotly for data visualization
import plotly.graph_objs as go
from plotly.offline import plot


# Dashboard view (requires login)
@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(context, request))


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
                calc_num = round(calc_num / 2.5) * 2.5  # Round to nearest 2.5 kg
                calculated_dict[num] = max(calc_num, 0)  # Replace negative values with zero

            # Create the exercise plan for each week
            exercise_dict = {
                'Week 1': {
                    'Set 1': f'{calculated_dict[0.40]}kg x 5',
                    'Set 2': f'{calculated_dict[0.65]}kg x 5',
                    'Set 3': f'{calculated_dict[0.75]}kg x 5',
                    'Set 4': f'{calculated_dict[0.85]}kg x 5',
                },
                'Week 2': {
                    'Set 1': f'{calculated_dict[0.40]}kg x 3',
                    'Set 2': f'{calculated_dict[0.70]}kg x 3',
                    'Set 3': f'{calculated_dict[0.80]}kg x 3',
                    'Set 4': f'{calculated_dict[0.90]}kg x 3',
                },
                'Week 3': {
                    'Set 1': f'{calculated_dict[0.40]}kg x 5',
                    'Set 2': f'{calculated_dict[0.75]}kg x 5',
                    'Set 3': f'{calculated_dict[0.85]}kg x 3',
                    'Set 4': f'{calculated_dict[0.95]}kg x 1',
                },
                'Week 4': {
                    'Set 1': f'{calculated_dict[0.40]}kg x 5',
                    'Set 2': f'{calculated_dict[0.40]}kg x 5',
                    'Set 3': f'{calculated_dict[0.50]}kg x 5',
                    'Set 4': f'{calculated_dict[0.60]}kg x 5',
                }
            }

            global_wendler_list = exercise_dict

            # Save the plan to the database
            plan = WendlerPlan.objects.create(
                user=request.user,
                name=form.cleaned_data.get('name', 'Default Wendler Plan'),
                weight=number,
                exercise_data=json.dumps(exercise_dict)
            )

            return render(request, 'home/wendler.html', {'form': form, 'number': number, 'calculated_dict': exercise_dict})
    else:
        form = WendlerForm()

    return render(request, 'home/wendler.html', {'form': form})


# View to generate PDF of the Wendler plan
def some_view(request):
    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    buffer = io.BytesIO()
    canv = canvas.Canvas(buffer)

    # Prepare data for the PDF table
    table_data = [['Week No.', 'Set 1', "Set 2", "Set 3", "Set 4"]]
    for week in range(1, 5):
        table_data.append([f'Week {week}'] + list(global_wendler_list[f'Week {week}'].values()))

    # Create header and table for PDF
    header = Paragraph("<bold><font size=18>Wendler Exercise List</font></bold>", style)
    table = Table(table_data)
    table.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))

    for each in range(len(table_data)):
        bg_color = colors.whitesmoke if each % 2 == 0 else colors.lightgrey
        table.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))

    aW, aH = 540, 720
    w, h = header.wrap(aW, aH)
    header.drawOn(canv, 72, 800)
    aH -= h
    w, h = table.wrap(aW, aH)
    table.drawOn(canv, 72, aH - h)
    canv.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='WendlerSheet.pdf')


# View to generate a Word document of the Wendler plan
def word_doc_view(request):
    document = Document()
    docx_title = "WendlerSheet.docx"
    document.add_paragraph("Wendler Exercise List")

    for week in range(1, 5):
        document.add_paragraph(f'Week {week}: {global_wendler_list[f"Week {week}"]}')

    document.add_page_break()

    f = io.BytesIO()
    document.save(f)
    length = f.tell()
    f.seek(0)
    return HttpResponse(f.getvalue(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        headers={'Content-Disposition': f'attachment; filename={docx_title}', 'Content-Length': length})


# View for displaying a list of Wendler plans
def wendler_plan_list(request):
    wendler_plans = WendlerPlan.objects.filter(user=request.user)
    for plan in wendler_plans:
        if isinstance(plan.exercise_data, str):
            try:
                plan.exercise_data = json.loads(plan.exercise_data)
            except json.JSONDecodeError:
                plan.exercise_data = {}
    return render(request, 'home/settings.html', {'wendler_plans': wendler_plans})


# View to update a Wendler plan
def update_wendler_plan(request, plan_id):
    plan = get_object_or_404(WendlerPlan, id=plan_id, user=request.user)

    if request.method == 'POST':
        form = WendlerPlanForm(request.POST, instance=plan)
        if form.is_valid():
            updated_plan = form.save(commit=False)
            updated_plan.updated_at = timezone.now()
            updated_plan.save()
            return redirect('wendler_plan_list')
    else:
        form = WendlerPlanForm(instance=plan)

    return render(request, 'home/update_wendler_plan.html', {'form': form, 'plan': plan})


# View to delete a Wendler plan
def delete_wendler_plan(request, plan_id):
    plan = get_object_or_404(WendlerPlan, id=plan_id, user=request.user)

    if request.method == 'POST':
        plan.delete()
        return redirect('wendler_plan_list')

    return render(request, 'home/confirm_delete.html', {'plan': plan})


# View to display performance data using CSV and Plotly
@login_required(login_url="/login/")
def pages(request):
    csv_files = ['benchpress.csv', 'age_skill_levels_deadlift.csv', 'age_skill_levels_overheadpress.csv', 'age_skill_levels_squat.csv']
    plot_divs, file_errors = [], []

    for file_name in csv_files:
        file_path = os.path.join(settings.DATA_DIR, 'apps', 'dataset', file_name)

        try:
            with open(file_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                csv_data = list(csv_reader)

                age = [int(row['Age']) for row in csv_data]
                categories = ['Beginner', 'Novice', 'Intermediate', 'Advanced', 'Elite']
                traces = [go.Scatter(x=age, y=[int(row[cat]) for row in csv_data], mode='lines', name=cat) for cat in categories]

                layout = go.Layout(title=f'{file_name.split(".")[0].capitalize()} Skill Levels', xaxis=dict(title='Age'), yaxis=dict(title='Weight'))
                figure = go.Figure(data=traces, layout=layout)
                plot_div = plot(figure, output_type='div', include_plotlyjs=False)
                plot_divs.append(plot_div)

        except FileNotFoundError:
            file_errors.append(file_name)

    context = {
        'segment': 'index',
        'plot_divs': plot_divs,
        'file_errors': file_errors,
    }

    return render(request, 'home/index.html', context)


# View for a specific page
def page(request, template):
    context = {}
    try:
        load_template = template + '.html'
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
