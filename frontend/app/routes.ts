import { route, type RouteConfig, index, prefix, layout } from "@react-router/dev/routes";

export default [
    layout("layouts/default.tsx", [
        ...prefix("job-boards", [
            route("/", "routes/job_boards.tsx"),
            route(":companyName/job-posts", "routes/job_posts.tsx"),
            route("/new", "routes/new_job_board.tsx"),
            route(":companyName/edit", "routes/update_job_board.tsx")
        ]),
        route("/", "routes/home.tsx") // route, the component we need to render
    ])
] satisfies RouteConfig;


