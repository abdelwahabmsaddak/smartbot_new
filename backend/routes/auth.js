import express from "express";
import bcrypt from "bcrypt";
import { db } from "../db.js";

const router = express.Router();

router.post("/register", async (req, res) => {
  const { full_name, email, password, referred_by } = req.body;

  const hashed = await bcrypt.hash(password, 10);

  const freeMonth = new Date();
  freeMonth.setMonth(freeMonth.getMonth() + 1);

  const affiliateCode = Math.random().toString(36).substring(2, 8).toUpperCase();

  try {
    await db.query(
      `INSERT INTO users (full_name, email, password_hash, free_trial_until, affiliate_code, referred_by)
       VALUES (?, ?, ?, ?, ?, ?)`,
      [full_name, email, hashed, freeMonth, affiliateCode, referred_by]
    );

    res.json({ status: "success", message: "User registered with 1-month free trial" });

  } catch (err) {
    res.json({ status: "error", message: err.message });
  }
});

export default router;
