import type { Route } from "../+types/root"; //@ts-ignore
import { Field, FieldGroup, FieldLabel, FieldLegend } from "~/components/ui/field"; //@ts-ignore
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";
import { Avatar, AvatarImage } from "~/components/ui/avatar";
import {Form, Link, redirect} from "react-router";


export async function clientLoader({params}: any) {

  const res = await fetch(`/api/job-boards/${params.companyName}`);

  const jobPosts = await res.json();
//   console.log(jobPosts)
  return {jobPosts};
}

export async function clientAction({ request }: Route.ClientActionArgs) {
  const formData = await request.formData()
  console.log(formData)
  await fetch('/api/job-boards/update', {
    method: 'PUT',
    body: formData,
  }) 
  return redirect('/job-boards')
}

export default function updateBoardForm({ loaderData }: any) {
    // console.log(loaderData)
    return (
    <div className="w-full max-w-4xl">
      <div className="flex gap-8 items-start">
        {/* Form Section - Left */}
        <div className="flex-1 max-w-md">
          <Form method="post" encType="multipart/form-data">
            <FieldGroup>
              <FieldLegend>Update Job Board</FieldLegend>
              <Field>
                <FieldLabel htmlFor="slug">
                  Slug
                </FieldLabel>
                <Input
                  id="slug"
                  name="slug"
                  value={loaderData.jobPosts.slug}
                  readOnly
                />
              </Field>
              <Field>
                <FieldLabel htmlFor="logo">
                  Logo
                </FieldLabel>
                <Input
                  id="logo"
                  name="logo"
                  type="file"
                  required
                />
              </Field>
              <div className="float-right">
                <Field orientation="horizontal">
                  <Button type="submit">Submit</Button>
                  <Button variant="outline" type="button">
                    <Link to="/job-boards">Cancel</Link>
                  </Button>
                </Field>
              </div>
            </FieldGroup>
          </Form>
        </div>

        {/* Avatar Section - Right */}
        <div className="flex-shrink-0">
          <Avatar className="w-32 h-32">
            <AvatarImage src={loaderData.jobPosts.logo_url} />
          </Avatar>
        </div>
      </div>
    </div>
  );
}