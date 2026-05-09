import { ButtonHTMLAttributes } from "react";

export default function Button(props: ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      className="rounded bg-slate-900 px-4 py-2 text-white disabled:opacity-50"
      {...props}
    />
  );
}
