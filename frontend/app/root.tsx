import { Outlet } from "react-router";

export default function App() {
  return (
    <html lang="en">
    <head>
      <title>Jobify</title>
    </head>
    <body>
      <Outlet />
    </body>
    </html>
);
}
