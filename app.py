
import gradio as gr

from physics_engine import (
    simulate,
    compare_mass_doubling
)

from ai_engine import (
    identify_concept,
    generate_explanation,
    DEFAULT_CONCEPT
)

from visualization import (
    create_motion_html,
    create_graph,
    create_dashboard
)


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def concept_card(concept):

    variables = ", ".join(
        concept.get("variables", [])
    )

    return f"""
### AI Concept Card

**Concept:** {concept.get("topic", "Newtonian Mechanics")}

**Equation:** `{concept.get("equation", "F = ma")}`

**Variables:** {variables}

**Independent variable:** {concept.get("independent_variable", "Mass")}

**Dependent variable:** {concept.get("dependent_variable", "Acceleration")}

**Recommended simulation:** {concept.get("recommended_simulation", "Force & Motion Lab")}

> {concept.get("short_explanation", "")}
"""


# ---------------------------------------------------------
# Analyze student question
# ---------------------------------------------------------

def analyze_question(
    question,
    mass,
    force,
    friction,
    initial_velocity
):

    if not str(question).strip():

        question = (
            "Why does a heavier object accelerate less "
            "when the same force is applied?"
        )

    concept, status = identify_concept(
        question
    )

    result = simulate(
        mass,
        force,
        friction,
        initial_velocity
    )

    return (

        concept_card(concept),

        status,

        create_motion_html(result),

        create_graph(result),

        create_dashboard(result),

        concept.get(
            "prediction_question",
            DEFAULT_CONCEPT["prediction_question"]
        ),

        "Make a prediction after changing the experiment controls.",

        "Run an experiment, make a prediction, and compare it with the physics engine.",

        []
    )


# ---------------------------------------------------------
# Update simulation when sliders move
# ---------------------------------------------------------

def update_simulation(
    mass,
    force,
    friction,
    initial_velocity
):

    result = simulate(
        mass,
        force,
        friction,
        initial_velocity
    )

    return (
        create_motion_html(result),
        create_graph(result),
        create_dashboard(result),
        result
    )


# ---------------------------------------------------------
# Prediction evaluation
# ---------------------------------------------------------

def evaluate_prediction(
    selected_answer,
    mass,
    force,
    friction,
    initial_velocity,
    question,
    history
):

    baseline, doubled, relation = compare_mass_doubling(
        mass,
        force,
        friction,
        initial_velocity
    )

    answer_labels = {

        "A": "Acceleration doubles",

        "B": "Acceleration becomes half",

        "C": "Acceleration stays the same"
    }

    student_answer = answer_labels.get(
        selected_answer,
        "No answer selected"
    )

    # For the intended Newton's Second Law demonstration
    # with zero friction:
    #
    # a = F / m
    #
    # Doubling mass makes acceleration half.

    if abs(friction) < 1e-12:

        if relation == "decreases":
            correct_answer = "B"

        elif relation == "increases":
            correct_answer = "A"

        else:
            correct_answer = "C"

    else:

        # When friction exists, derive the answer from
        # the deterministic simulation itself.
        if relation == "increases":
            correct_answer = "A"

        elif relation == "decreases":
            correct_answer = "B"

        else:
            correct_answer = "C"


    correct = (
        selected_answer == correct_answer
    )


    if correct:

        status = f"""
### ✅ Correct!

The deterministic physics engine says acceleration
**{relation}** when the mass is doubled.

Your prediction:

**{student_answer}**
"""

    else:

        status = f"""
### ❌ Not quite

The deterministic physics engine says acceleration
**{relation}** when the mass is doubled.

Your prediction:

**{student_answer}**
"""


    parameters = {

        "mass": mass,

        "applied_force": force,

        "friction_coefficient": friction,

        "initial_velocity": initial_velocity
    }


    explanation = generate_explanation(

        question,

        parameters,

        baseline,

        student_answer,

        correct
    )


    experiment_number = len(history) + 1

    record = (
        f"**Experiment {experiment_number}:** "
        f"Mass = {mass:.1f} kg · "
        f"Force = {force:.1f} N · "
        f"Friction = {friction:.2f} · "
        f"Acceleration = {baseline['acceleration']:.2f} m/s²"
    )


    new_history = history + [record]


    return (

        status,

        explanation,

        "\n\n".join(new_history),

        new_history
    )


# ---------------------------------------------------------
# Suggested next experiment
# ---------------------------------------------------------

def suggest_next_experiment(
    mass,
    force,
    friction,
    initial_velocity
):

    if force <= 25:

        new_force = force * 2

    else:

        new_force = force / 2

    return f"""
### Try Next Experiment

Keep the mass at **{mass:.1f} kg**.

Keep friction at **{friction:.2f}**.

Change force from:

**{force:.1f} N → {new_force:.1f} N**

Before running it, predict:

> What will happen to acceleration?
"""


# ---------------------------------------------------------
# UI CSS
# ---------------------------------------------------------

CSS = """

.gradio-container {
    max-width: 1180px !important;
    margin: auto !important;
}

.hero {
    padding: 28px;
    border-radius: 22px;
    background: linear-gradient(
        135deg,
        #111827,
        #1e293b
    );
    color: white;
    margin-bottom: 16px;
}

.hero h1 {
    font-size: 36px;
    margin-bottom: 6px;
}

.hero p {
    color: #cbd5e1;
    font-size: 16px;
}

"""



# ---------------------------------------------------------
# Initial simulation
# ---------------------------------------------------------

initial_result = simulate(
    2,
    10,
    0,
    0
)


# ---------------------------------------------------------
# Gradio Application
# ---------------------------------------------------------

with gr.Blocks(
    css=CSS,
    title="Dr.Agentic — Physics Lab"
) as demo:


    # -------------------------------
    # State
    # -------------------------------

    result_state = gr.State(
        initial_result
    )

    history_state = gr.State(
        []
    )


    # -------------------------------
    # Header
    # -------------------------------

    gr.HTML(
        """
        <div class="hero">

            <h1>
                Dr.Agentic — Physics Lab
            </h1>

            <p>
                Ask. Experiment. Discover.
                &nbsp; • &nbsp;
                Turn physics questions into experiments.
            </p>

        </div>
        """
    )


    # -------------------------------
    # ASK
    # -------------------------------

    with gr.Row():

        with gr.Column(
            scale=2
        ):

            question = gr.Textbox(

                label="1 · ASK",

                value=(
                    "Why does a heavier object accelerate "
                    "less when the same force is applied?"
                ),

                lines=3,

                placeholder=(
                    "Ask a Newtonian force & motion question..."
                )
            )


            gr.Examples(

                examples=[

                    [
                        "Why does a heavier object accelerate less when the same force is applied?"
                    ],

                    [
                        "What happens if I increase the force while keeping mass constant?"
                    ],

                    [
                        "How does friction affect acceleration?"
                    ],

                    [
                        "What happens to velocity if acceleration stays positive?"
                    ]

                ],

                inputs=question
            )


            analyze_button = gr.Button(
                "Analyze Question →",
                variant="primary"
            )


        with gr.Column(
            scale=1
        ):

            concept = gr.Markdown(
                concept_card(DEFAULT_CONCEPT)
            )

            ai_status = gr.Markdown(
                "Fallback lesson ready. "
                "Add GROQ_API_KEY to enable AI orchestration."
            )


    # -------------------------------
    # SIMULATION
    # -------------------------------

    gr.Markdown(
        "## 2 · Force & Motion Lab"
    )


    with gr.Row():


        # Controls
        with gr.Column(
            scale=1
        ):

            gr.Markdown(
                "### Experiment Controls"
            )


            mass = gr.Slider(

                minimum=0.1,
                maximum=10,

                value=2,

                step=0.1,

                label="Mass (kg)"
            )


            force = gr.Slider(

                minimum=0,
                maximum=50,

                value=10,

                step=0.5,

                label="Applied Force (N)"
            )


            friction = gr.Slider(

                minimum=0,
                maximum=1,

                value=0,

                step=0.01,

                label="Friction coefficient (μ)"
            )


            initial_velocity = gr.Slider(

                minimum=-10,
                maximum=20,

                value=0,

                step=0.5,

                label="Initial velocity (m/s)"
            )


            run_again = gr.Button(
                "Run Experiment Again",
                variant="primary"
            )


            next_experiment = gr.Button(
                "Try Next Experiment"
            )


            next_experiment_text = gr.Markdown()


        # Visualization
        with gr.Column(
            scale=2
        ):

            motion = gr.HTML(
                create_motion_html(
                    initial_result
                )
            )


            graph = gr.Plot(
                create_graph(
                    initial_result
                )
            )


            dashboard = gr.Markdown(
                create_dashboard(
                    initial_result
                )
            )


    # -------------------------------
    # PREDICTION
    # -------------------------------

    gr.Markdown(
        "## 3 · Prediction Challenge"
    )


    prediction_question = gr.Markdown(
        DEFAULT_CONCEPT[
            "prediction_question"
        ]
    )


    with gr.Row():

        answer_a = gr.Button(
            "A · Acceleration doubles"
        )

        answer_b = gr.Button(
            "B · Acceleration becomes half"
        )

        answer_c = gr.Button(
            "C · Acceleration stays the same"
        )


    prediction_status = gr.Markdown(
        "Choose an answer after experimenting."
    )


    explanation = gr.Markdown(
        "Run an experiment, make a prediction, "
        "then see the evidence-based explanation."
    )


    # -------------------------------
    # HISTORY
    # -------------------------------

    gr.Markdown(
        "## 4 · Experiment History"
    )


    history_display = gr.Markdown(
        "No experiments recorded yet."
    )


    # =====================================================
    # EVENT HANDLERS
    # =====================================================


    # Analyze question
    analyze_button.click(

        analyze_question,

        inputs=[
            question,
            mass,
            force,
            friction,
            initial_velocity
        ],

        outputs=[

            concept,
            ai_status,
            motion,
            graph,
            dashboard,
            prediction_question,
            prediction_status,
            explanation,
            history_state
        ]
    )


    # Update simulation immediately when controls change.
    for control in [
        mass,
        force,
        friction,
        initial_velocity
    ]:

        control.change(

            update_simulation,

            inputs=[
                mass,
                force,
                friction,
                initial_velocity
            ],

            outputs=[
                motion,
                graph,
                dashboard,
                result_state
            ]
        )


    # Run experiment again.
    run_again.click(

        update_simulation,

        inputs=[
            mass,
            force,
            friction,
            initial_velocity
        ],

        outputs=[
            motion,
            graph,
            dashboard,
            result_state
        ]
    )


    # Suggested experiment.
    next_experiment.click(

        suggest_next_experiment,

        inputs=[
            mass,
            force,
            friction,
            initial_velocity
        ],

        outputs=[
            next_experiment_text
        ]
    )


    # Prediction buttons.
    answer_a.click(

        lambda m, f, fr, u, q, h:
            evaluate_prediction(
                "A",
                m,
                f,
                fr,
                u,
                q,
                h
            ),

        inputs=[
            mass,
            force,
            friction,
            initial_velocity,
            question,
            history_state
        ],

        outputs=[
            prediction_status,
            explanation,
            history_display,
            history_state
        ]
    )


    answer_b.click(

        lambda m, f, fr, u, q, h:
            evaluate_prediction(
                "B",
                m,
                f,
                fr,
                u,
                q,
                h
            ),

        inputs=[
            mass,
            force,
            friction,
            initial_velocity,
            question,
            history_state
        ],

        outputs=[
            prediction_status,
            explanation,
            history_display,
            history_state
        ]
    )


    answer_c.click(

        lambda m, f, fr, u, q, h:
            evaluate_prediction(
                "C",
                m,
                f,
                fr,
                u,
                q,
                h
            ),

        inputs=[
            mass,
            force,
            friction,
            initial_velocity,
            question,
            history_state
        ],

        outputs=[
            prediction_status,
            explanation,
            history_display,
            history_state
        ]
    )


# ---------------------------------------------------------
# Launch
# ---------------------------------------------------------

demo.launch(
    share=True,
    debug=True
)
