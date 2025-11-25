import {useState, useEffect} from "react";
import {Link} from "react-router";

export async function clientLoader() { // keyword determining this is a loader function. We are not calling it manually. It's similar to a keyword
  const res = await fetch(`/api/job-boards`);
  const jobBoards = await res.json();
  return {jobBoards}
}

export default function JobBoards({loaderData}: any) {
  return (
    <div>
      {loaderData.jobBoards.map(
        (jobBoard: any) => 
              <div style={{
                  display: "flex",
                  flexWrap: "wrap"
              }}>
                  <p key={jobBoard.id}>
                      <Link to={`/job-boards/${jobBoard.slug}/job-posts`}>{jobBoard.slug}</Link>
                  </p>
                  <img src={jobBoard.logo_url} style={{
                    width: "100px",
                    height: "100px"
                  }}></img>
              </div>
      )}
    </div>
  )
}   