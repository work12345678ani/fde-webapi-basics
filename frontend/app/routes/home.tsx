import { Link } from "react-router"
export default function home() {
    return (
        <div>
            <h1>Welcome to Jobify!</h1>
            <Link to="/job-boards">Go To Job Boards</Link>
        </div>
    )
}