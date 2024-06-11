import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs) {
  return twMerge(clsx(inputs))
}

// @/lib/utils.js
// export const cn = (...classNames) => classNames.filter(Boolean).join(" ");