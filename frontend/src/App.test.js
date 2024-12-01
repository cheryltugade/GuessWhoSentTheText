import { render, screen } from '@testing-library/react';
import App from './App';

test('renders learn react link', () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});

  // let originalTexts = [
  //   {text: "So I am not tagged.", sender: 'Cheryl'},
  //   {text: "And now I am listening to the goss", sender: 'Mallika'},
  //   {text: "Hi chennupaty!", sender: 'Cheryl'},
  //   {text: "What ru going to do", sender: 'Mallika'},
  //   {text: "I put one PR out today", sender: 'Mallika'},
  //   {text: "And I hope ur sleep improves", sender: 'Cheryl'},
  // ]
  // let userName = 'Cheryl'
  // let contactName = 'Mallika'
