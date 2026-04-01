import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

circle1_center = (0.5, 0.5)
circle1_radius = 0.3
circle2_center = (0.7, 0.5)
circle2_radius = 0.3
def draw_euler_diagram(ax, alpha_intersection=0.5, alpha_circle1=0.3, alpha_circle2=0.3, union_mode=None):

    ax.clear()
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    text_color = 'black'

    circle1_patch = plt.Circle(circle1_center, circle1_radius, color='blue', alpha=alpha_circle1, fill=True)
    ax.add_patch(circle1_patch)
    ax.text(circle1_center[0] - circle1_radius * 0.6, circle1_center[1] + circle1_radius * 0.8, 'A', fontsize=14, color=text_color, ha='center', va='center')

    circle2_patch = plt.Circle(circle2_center, circle2_radius, color='red', alpha=alpha_circle2, fill=True)
    ax.add_patch(circle2_patch)
    ax.text(circle2_center[0] + circle2_radius * 0.6, circle2_center[1] + circle2_radius * 0.8, 'B', fontsize=14, color=text_color, ha='center', va='center')

    if union_mode is None:
        x, y = np.meshgrid(np.linspace(0, 1, 200), np.linspace(0, 1, 200))
        dist1_sq = (x - circle1_center[0])**2 + (y - circle1_center[1])**2
        dist2_sq = (x - circle2_center[0])**2 + (y - circle2_center[1])**2

        intersection_mask = (dist1_sq <= circle1_radius**2) & (dist2_sq <= circle2_radius**2)

        intersection_color = 'green'
        ax.imshow(np.where(intersection_mask, 1, 0), extent=[0, 1, 0, 1],
                  cmap=plt.cm.colors.ListedColormap(['none', intersection_color]),
                  alpha=alpha_intersection, zorder=10)

    if union_mode == 'single_color_with_borders':
        ax.clear()
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        union_color = 'purple'

        x, y = np.meshgrid(np.linspace(0, 1, 200), np.linspace(0, 1, 200))
        dist1_sq = (x - circle1_center[0])**2 + (y - circle1_center[1])**2
        dist2_sq = (x - circle2_center[0])**2 + (y - circle2_center[1])**2

        union_mask = (dist1_sq <= circle1_radius**2) | (dist2_sq <= circle2_radius**2)

        ax.imshow(np.where(union_mask, 1, 0), extent=[0, 1, 0, 1],
                  cmap=plt.cm.colors.ListedColormap(['none', union_color]),
                  alpha=0.6, zorder=1)

        circle1_outline = plt.Circle(circle1_center, circle1_radius, color='blue', fill=False, linewidth=2, zorder=2)
        ax.add_patch(circle1_outline)
        ax.text(circle1_center[0] - circle1_radius * 0.6, circle1_center[1] + circle1_radius * 0.8, 'A', fontsize=14, color=text_color, ha='center', va='center', zorder=3)

        circle2_outline = plt.Circle(circle2_center, circle2_radius, color='red', fill=False, linewidth=2, zorder=2)
        ax.add_patch(circle2_outline)
        ax.text(circle2_center[0] + circle2_radius * 0.6, circle2_center[1] + circle2_radius * 0.8, 'B', fontsize=14, color=text_color, ha='center', va='center', zorder=3)

        ax.set_title("Объединение (A ∪ B)")

def show_intersection_with_borders(event):
    draw_euler_diagram(ax, alpha_intersection=0.8, alpha_circle1=0.1, alpha_circle2=0.1, union_mode=None)
    ax.set_title("Пересечение (A ∩ B)")
    fig.canvas.draw_idle()

def show_union_combined_with_borders(event):
    draw_euler_diagram(ax, union_mode='single_color_with_borders')
    fig.canvas.draw_idle()

def show_difference1(event): # A \ B
    ax.clear()
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Разность множеств (A \\ B)")
    ax.axis('off')

    text_color = 'black'

    circle1_only = plt.Circle(circle1_center, circle1_radius, color='blue', alpha=0.5, fill=True)
    ax.add_patch(circle1_only)
    ax.text(circle1_center[0] - circle1_radius * 0.6, circle1_center[1] + circle1_radius * 0.8, 'A', fontsize=14, color=text_color, ha='center', va='center')


    circle2_outline = plt.Circle(circle2_center, circle2_radius, color='red', alpha=0.3, fill=False, linestyle='dashed')
    ax.add_patch(circle2_outline)
    fig.canvas.draw_idle()

def show_difference2(event): # B \ A
    ax.clear()
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Разность множеств (B \\ A)")
    ax.axis('off')

    text_color = 'black'

    circle2_only = plt.Circle(circle2_center, circle2_radius, color='red', alpha=0.5, fill=True)
    ax.add_patch(circle2_only)
    ax.text(circle2_center[0] + circle2_radius * 0.6, circle2_center[1] + circle2_radius * 0.8, 'B', fontsize=14, color=text_color, ha='center', va='center')

    circle1_outline = plt.Circle(circle1_center, circle1_radius, color='blue', alpha=0.3, fill=False, linestyle='dashed')
    ax.add_patch(circle1_outline)
    fig.canvas.draw_idle()

def show_all(event):
    draw_euler_diagram(ax, alpha_intersection=0.5, alpha_circle1=0.3, alpha_circle2=0.3, union_mode=None)
    ax.set_title("Круги Эйлера (A и B)")
    fig.canvas.draw_idle()

fig, ax = plt.subplots(figsize=(8, 6))

draw_euler_diagram(ax)
ax.set_title("Круги Эйлера (A и B)")

button_y_start = 0.1
button_height = 0.08
button_width = 0.2
button_spacing = 0.02

rect_all = plt.axes([0.05, button_y_start, button_width, button_height])
button_all = Button(rect_all, 'Круги Эйлера')
button_all.on_clicked(show_all)

rect_intersection = plt.axes([0.05, button_y_start + button_height + button_spacing, button_width, button_height])
button_intersection = Button(rect_intersection, 'Пересечение (A ∩ B)')
button_intersection.on_clicked(show_intersection_with_borders)

rect_union_combined = plt.axes([0.05, button_y_start + 2 * (button_height + button_spacing), button_width, button_height])
button_union_combined = Button(rect_union_combined, 'Объединение (A ∪ B)')
button_union_combined.on_clicked(show_union_combined_with_borders)

rect_difference1 = plt.axes([0.05, button_y_start + 3 * (button_height + button_spacing), button_width, button_height])
button_difference1 = Button(rect_difference1, 'Разность (A \\ B)')
button_difference1.on_clicked(show_difference1)

rect_difference2 = plt.axes([0.05, button_y_start + 4 * (button_height + button_spacing), button_width, button_height])
button_difference2 = Button(rect_difference2, 'Разность (B \\ A)')
button_difference2.on_clicked(show_difference2)

plt.show()
