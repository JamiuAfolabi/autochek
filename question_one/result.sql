
with repayment AS
	(
		select 
			loan_id_fk,
			cast("Amount_paid" as date) as date_paid,
			"Date_paid" as amount_paid,
			regexp_replace(payment_id_pk,'PAID','') as schedule_key
		from
			public.repayment_data
	)	
	
	select 
		l.loan_id,
		b."Borrower_Id" as borrower_id,
		l."Date_of_release" as loan_date_of_release,
		l."Term" as term,
		l."LoanAmount",
		l."Downpayment",
		b."State" as state,
		b."City" as city,
		b."zip code",
		l."Payment_frequency" payment_frequency,
		l."Maturity_date" as maturity_date,
		(r.date_paid - p."Expected_payment_date") as current_days_past_due, 
		p."Expected_payment_date" as last_due_date, 
		r.date_paid as last_repayment_date, 
		Sum(
			case 
				when r.date_paid > p."Expected_payment_date" 
			THEN	
				p."Expected_payment_amount"
			ELSE
				0
			end) over(partition by b."Borrower_Id",l.loan_id,extract(month from r.date_paid),extract(year from r.date_paid) order by p."Expected_payment_date" )	as amount_at_risk_date_paid,
		b.borrower_credit_score, 
		null as branch, 
		null as branch_id,  
		null as borrower_name, 
 		sum(r.amount_paid) over(partition by b."Borrower_Id",l.loan_id order by r.date_paid rows between unbounded preceding and current row) total_amount_paid,  
 		sum(p."Expected_payment_amount") over(partition by b."Borrower_Id",l.loan_id order by p."Expected_payment_date" rows between unbounded preceding and current row)  total_amount_expected
	from
		repayment r 
	inner join 
		public.loan_data l 
	on
		r.loan_id_fk = l.loan_id 
	inner join
		public.payment_schedule p 
	on
		p.loan_id = r.loan_id_fk 
		and 
		r.schedule_key = p.schedule_id  
	inner join 
		public.borrower b  
	on 
		b."Borrower_Id" = l."Borrower_id"