// JobBoardPosts.tsx
import { useParams } from "react-router";
export async function clientLoader({params}: any) {

  const res = await fetch(`/api/job-boards/${params.companyName}/job-posts`);

  const jobPosts = await res.json();
//   console.log(jobPosts)
  return {jobPosts};
}

export default function JobBoardPosts({loaderData}:any) {

  return (
    <div>
      {loaderData.jobPosts.map((post: any) => (
        <div  key={post.id}>
            <h1>{post.title}</h1>
            <p>Description: {post.description}</p>
            <p>Location: {post.location}</p> 
        </div>
      ))}
    </div>
  );
}
