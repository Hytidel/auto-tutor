# Lesson 1: The Concept and Geometric Meaning of Derivatives

**Time**: 2026-04-06-22-00
**Topic**: Differential Calculus of Functions of One Variable
**Target Cognitive Level**: Understand/Apply

---

## Learning Objectives

After completing this lesson, you should be able to:
- Understand the concept of derivative as the limit of a difference quotient
- Explain the geometric meaning of derivative as the slope of a tangent line
- Distinguish between one-sided derivatives and understand the condition for derivability
- Apply the relationship between derivability and continuity

---

## Content

### 1. The Concept of Rate of Change

In calculus, we often encounter problems related to the "rate of change" of functions. Whether it's instantaneous velocity in physics, marginal utility in economics, or the slope of a curve's tangent line, they all fundamentally concern the rate of change of functions.

Let a function $f$ be defined on a neighborhood $N_r(x_0)$ of $x_0$. When the independent variable changes from $x_0$ to $x_0 + \Delta x$, we call $\Delta x$ the **increment** of the independent variable at $x_0$. Let $\Delta f(x) = f(x) - f(x_0)$. We call $\Delta f(x)$ the **increment** or **difference** of the function $f(x)$ at $x_0$.

The quotient of the function's difference and the increment of the independent variable at $x_0$ is called the **difference quotient** of $f(x)$ at $x_0$:

$$\frac{f(x_0 + \Delta x) - f(x_0)}{\Delta x} = \frac{\Delta f(x)}{\Delta x}$$

[Source: Section 5.1.1 The Concept of Derivative]

**Key Insight**: The problem of "average rate of change" reduces to calculating the difference quotient. If we want to know the "instantaneous rate of change" at $x_0$, we need to calculate the limit of the difference quotient as $\Delta x \to 0$.

---

### 2. Definition of Derivative

> **Original Text**:
> Let function $f(x)$ be defined on a neighborhood $N_r(x_0)$ of $x_0$. If there exists $a \in \mathbb{R}$ such that
> $$\lim_{\Delta x \to 0} \frac{f(x_0 + \Delta x) - f(x_0)}{\Delta x} = a$$
> then $f(x)$ is said to be **derivable** at $x_0$, and $a$ is called the **derivative** of $f$ at $x_0$, denoted as $f'(x_0) = a$.

**Alternative Form**: Let $x = x_0 + \Delta x$, then the definition becomes:

$$f'(x_0) := \lim_{x \to x_0} \frac{f(x) - f(x_0)}{x - x_0}$$

[Source: Definition 5.1 (Derivative)]

---

### 3. Geometric Meaning: Tangent Lines

We can now precisely define the tangent line to a curve. If the curve $y = f(x)$ is derivable at $x_0$, then the line passing through point $P(x_0, f(x_0))$ with slope $f'(x_0)$:

$$y = f(x_0) + f'(x_0)(x - x_0)$$

is called the **tangent line** to the curve $y = f(x)$ at $P$.

The line through $P$ perpendicular to the tangent line is called the **normal line** to the curve at $P$.

> **Geometric Insight**: The slope of the tangent line at a point is precisely the geometric meaning of the derivative. From a geometric perspective, being derivable at a point means the curve is "smooth" at that point—points with "corners" or "sharp edges" are not derivable and have no tangent lines.

[Source: Section 5.1.1 The Concept of Derivative]

---

### 4. One-sided Derivatives

Since we have one-sided limits, we can define one-sided derivatives:

> **Original Text**:
> - **Left Derivative**: If $f$ is defined on the left neighborhood $N_r^-(x_0)$, and there exists $a \in \mathbb{R}$ such that
> $$\lim_{\Delta x \to 0-} \frac{f(x_0 + \Delta x) - f(x_0)}{\Delta x} = a$$
> then $f$ is left-derivable at $x_0$, and $a$ is called the **left derivative**, denoted as $f'_-(x_0)$.
>
> - **Right Derivative**: Similarly, the **right derivative** $f'_+(x_0)$ is defined using the right-hand limit.

[Source: Definition 5.2 (One-sided Derivative)]

**Critical Proposition**: A function $f(x)$ is derivable at $x_0$ with $f'(x_0) = a$ if and only if:

$$f'_-(x_0) = f'_+(x_0) = a$$

[Source: Proposition 5.1]

---

### 5. The Relationship Between Derivability and Continuity

> **Original Text**:
> If a function $f(x)$ is derivable at $x_0$, then $f(x)$ is continuous at $x_0$.

**Proof**:
Since $f$ is derivable at $x_0$, we have:
$$\lim_{x \to x_0} [f(x) - f(x_0)] = \lim_{x \to x_0} \left[\frac{f(x) - f(x_0)}{x - x_0} \cdot (x - x_0)\right] = \lim_{x \to x_0} \frac{f(x) - f(x_0)}{x - x_0} \cdot \lim_{x \to x_0}(x - x_0) = 0$$

This shows $\lim_{x \to x_0} f(x) = f(x_0)$, so $f(x)$ is continuous at $x_0$.

[Source: Theorem 5.1 (Relationship between Derivability and Continuity)]

---

### 🔍 Counterfactual Reasoning Section

**Question**: What if a function did NOT satisfy the condition of being derivable? What would be the consequence?

**Analysis**: If a function fails to be derivable at a point, it could be due to:
1. The function being discontinuous at that point (contradiction to the theorem above)
2. The function being continuous but having different left and right derivatives

**Edge Case - The Absolute Value Function**:

> **Original Text**: The function $f(x) = |x|$ is not derivable at $x = 0$.

**Proof**:
$$f'_+(0) = \lim_{\Delta x \to 0+} \frac{f(\Delta x) - f(0)}{\Delta x} = \lim_{\Delta x \to 0+} \frac{\Delta x}{\Delta x} = 1$$
$$f'_-(0) = \lim_{\Delta x \to 0-} \frac{f(\Delta x) - f(0)}{\Delta x} = \lim_{\Delta x \to 0-} \frac{-\Delta x}{\Delta x} = -1$$

Since $f'_+(0) \neq f'_-(0)$, the function $f(x) = |x|$ is not derivable at $x = 0$.

[Source: Example 5.1]

**Counterfactual Insight**: This example shows that **continuity is necessary but NOT sufficient for derivability**. The absolute value function is continuous everywhere but has a "corner" at $x = 0$, making it non-derivable there.

---

### 6. Calculating Derivatives from Definition

**Example: Constant Function**
If $f(x) = C$ for all $x$, then $f'(x) = 0$.

[Source: Example 5.4]

**Example: Power Function**
For $f(x) = x^m$ where $m \in \mathbb{N}^*$, using the definition:
$$f'(x_0) = \lim_{x \to x_0} \frac{x^m - x_0^m}{x - x_0} = mx_0^{m-1}$$

Thus, $(x^m)' = mx^{m-1}$ for all $x \in \mathbb{R}$.

[Source: Example 5.5]

---

## Practice Problems

> Please fill in your answers in the "My Answer" section for each problem. Save the file and tell me "completed" in the chat.

### Problem 1: Understanding the Definition

Using the definition of derivative, explain why the derivative represents "instantaneous rate of change." What is the relationship between the difference quotient and the derivative?

[Source: Section 5.1.1]

**My Answer**:

---

### Problem 2: One-sided Derivatives

Consider the function:
$$g(x) = \begin{cases} x^2, & x \geq 0 \\ -x, & x < 0 \end{cases}$$

1. Is $g(x)$ continuous at $x = 0$?
2. Calculate $g'_-(0)$ and $g'_+(0)$.
3. Is $g(x)$ derivable at $x = 0$?

[Source: Definition 5.2, Proposition 5.1]

**My Answer**:

---

### Problem 3: Applying the Derivative Definition

Using the definition of derivative (limit of difference quotient), find the derivative of $f(x) = x^3$ at an arbitrary point $x_0$.

Hint: Use the factorization $a^3 - b^3 = (a-b)(a^2 + ab + b^2)$.

[Source: Example 5.5]

**My Answer**:

---

### Problem 4: The Derivability-Continuity Relationship

A student claims: "If a function is continuous at a point, then it must be derivable at that point."

1. Is this statement correct? Why or why not?
2. Give a counterexample if the statement is false.
3. What is the correct relationship between derivability and continuity?

[Source: Theorem 5.1, Example 5.1]

**My Answer**:

---

## Reflection

After completing this lesson, please answer:

1. **Cognitive Difficulty** (1-5): [ ] 1-Too Easy [ ] 2-Just Right [ ] 3-Somewhat Difficult [ ] 4-Very Difficult [ ] 5-Completely Lost
2. **Which parts need clarification?**:

---

## Key Takeaways

- **Derivative Definition**: The derivative $f'(x_0)$ is the limit of the difference quotient as $\Delta x \to 0$
- **Geometric Meaning**: The derivative equals the slope of the tangent line at that point
- **One-sided Derivatives**: Derivability requires left and right derivatives to be equal
- **Derivability vs Continuity**: Derivable $\Rightarrow$ Continuous, but NOT vice versa
- **The absolute value function** is the classic example of continuous but non-derivable

---

## Next Lesson Preview

In the next lesson, we will explore the **concept of differentials and the relationship between derivatives and differentials**, including:
- The infinitesimal increment formula
- Linear principal part and its meaning
- Derivative formulas for elementary functions
