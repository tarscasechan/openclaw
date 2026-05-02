import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import WelcomeCard from '../src/components/WelcomeCard.jsx';

function assertIncludes(label, html, expected) {
  if (!html.includes(expected)) {
    throw new Error(`${label}: expected rendered HTML to include ${JSON.stringify(expected)}. Got: ${html}`);
  }
}

const happyPath = renderToStaticMarkup(
  <WelcomeCard name="Ada" role="React components" isOnline={true} />
);

assertIncludes('happy path greeting', happyPath, 'Hello, Ada!');
assertIncludes('happy path role', happyPath, 'You are learning React components.');
assertIncludes('happy path status', happyPath, 'Ready to build');

const fallbackPath = renderToStaticMarkup(<WelcomeCard name="   " />);
assertIncludes('fallback greeting', fallbackPath, 'Hello, friend!');
assertIncludes('fallback status', fallbackPath, 'Taking it step by step');

console.log('smoke test passed');
