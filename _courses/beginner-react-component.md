---
title: Beginner Guide: Write a React Component
summary: Build one small reusable WelcomeCard component and learn the minimum concepts that make React useful.
example: courses/examples/beginner-react-component
---

# Beginner Guide: Write a React Component

You are going to build one small thing: a reusable `WelcomeCard`.

By the end, you will know the core shape of a React component:

```jsx
<ComponentName propName="value" />
```

The goal is not to learn all of React. The goal is to make one useful component, notice where plain HTML starts to hurt, and add only the React concepts that solve that pain.

## Lesson 1: Make a Card — component

**Outcome:** You can write a component function that returns markup.

Plain HTML is fine until you want to reuse the same chunk in more than one place. React starts with a function that returns UI.

Create `src/components/WelcomeCard.jsx`:

```jsx
import React from 'react';

export default function WelcomeCard() {
  return (
    <article className="card">
      <h2>Hello, Ada!</h2>
      <p>You are learning React components.</p>
      <p aria-label="status">🟢 Ready to build</p>
    </article>
  );
}
```

Then render it from `src/main.jsx`:

```jsx
import React from 'react';
import { createRoot } from 'react-dom/client';
import WelcomeCard from './components/WelcomeCard.jsx';

function App() {
  return (
    <main>
      <WelcomeCard />
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);
```

**Try it:** Run the app and check that the page says `Hello, Ada!`.

**What changed?** A component is just a reusable UI function.

**But:** This card always says Ada, so it is reusable only in theory.

## Lesson 2: Pass a Name — props

**Outcome:** You can pass data into a component with props.

Hard-coded text breaks as soon as the same card needs a different name. Props are the inputs to your component.

Update `WelcomeCard.jsx`:

```jsx
import React from 'react';

export default function WelcomeCard({ name }) {
  return (
    <article className="card">
      <h2>Hello, {name}!</h2>
      <p>You are learning React components.</p>
      <p aria-label="status">🟢 Ready to build</p>
    </article>
  );
}
```

Use it like this:

```jsx
<WelcomeCard name="Ada" />
<WelcomeCard name="Grace" />
```

**Try it:** Render two cards with two different names.

**What changed?** Props let one component produce different UI from different inputs.

**But:** If `name` is empty, the card says `Hello, !`, which feels broken.

## Lesson 3: Handle Missing Data — fallback

**Outcome:** You can protect a component from a weak input.

Real data is rarely perfect. A beginner component should handle one obvious failure case.

Update the component:

```jsx
import React from 'react';

export default function WelcomeCard({ name }) {
  const displayName = name?.trim() || 'friend';

  return (
    <article className="card">
      <h2>Hello, {displayName}!</h2>
      <p>You are learning React components.</p>
      <p aria-label="status">🟢 Ready to build</p>
    </article>
  );
}
```

**Try it:** Render `<WelcomeCard name="" />`.

Expected text:

```txt
Hello, friend!
```

**What changed?** A small fallback keeps the component useful when the input is blank.

**But:** The card still has one fixed status, even when the learner is not ready yet.

## Lesson 4: Show a State — conditional rendering

**Outcome:** You can show different UI when a prop changes.

React components often answer simple questions: if this is true, show one thing; otherwise, show another.

Update the component:

```jsx
import React from 'react';

export default function WelcomeCard({ name, isOnline = false }) {
  const displayName = name?.trim() || 'friend';

  return (
    <article className="card">
      <h2>Hello, {displayName}!</h2>
      <p>You are learning React components.</p>
      <p aria-label="status">
        {isOnline ? '🟢 Ready to build' : '⚪ Taking it step by step'}
      </p>
    </article>
  );
}
```

Use it like this:

```jsx
<WelcomeCard name="Ada" isOnline={true} />
<WelcomeCard name="Grace" />
```

**Try it:** Check that Ada gets the green status and Grace gets the gray status.

**What changed?** Conditional rendering lets one component cover more than one situation.

**But:** The lesson text is still hard-coded, so the card only works for React.

## Lesson 5: Make It Reusable — final props

**Outcome:** You can finish a small component with the inputs it truly needs.

The component needs one more input: what the learner is working on.

Final `WelcomeCard.jsx`:

```jsx
import React from 'react';

export default function WelcomeCard({ name, role, isOnline = false }) {
  const displayName = name?.trim() || 'friend';
  const lesson = role || 'React components';

  return (
    <article className="card">
      <h2>Hello, {displayName}!</h2>
      <p>You are learning {lesson}.</p>
      <p aria-label="status">
        {isOnline ? '🟢 Ready to build' : '⚪ Taking it step by step'}
      </p>
    </article>
  );
}
```

Use it like this:

```jsx
<WelcomeCard name="Ada" role="React components" isOnline={true} />
<WelcomeCard name="" />
```

Expected output includes:

```txt
Hello, Ada!
You are learning React components.
🟢 Ready to build

Hello, friend!
You are learning React components.
⚪ Taking it step by step
```

**Try it:** Change `role` to `CSS grid` and confirm only that sentence changes.

**What changed?** The component is now reusable because its variable parts are inputs.

**But:** If many cards share the same data shape, the next pain is rendering a list without copying the same line again and again.

## Minimal example artifact

The complete working example lives at:

```txt
courses/examples/beginner-react-component
```

Run it:

```bash
cd courses/examples/beginner-react-component
npm install
npm run dev
```

Smoke test it:

```bash
npm run build
npm run test:smoke
```

## Checklist / eval

A learner succeeds if they can:

- Explain that a component is a function that returns UI.
- Use JSX with `className`, not `class`.
- Pass a `name` prop into a component.
- Add a fallback for an empty `name`.
- Use a boolean prop for conditional rendering.
- Reuse the same component with different props.
- Verify one happy path and one fallback path.

## Cut list / next courses

Save these for later:

- `useState`
- event handlers
- lists and keys
- forms
- TypeScript props
- CSS modules / Tailwind
- component tests with Testing Library
