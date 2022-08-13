CREATE TABLE IF NOT EXISTS public.borrower
(
    "Borrower_Id" text NOT NULL,
    "State" text,
    "City" text,
    "zip code" bigint,
    borrower_credit_score text,
	 CONSTRAINT borrower_id_pk
			PRIMARY KEY ("Borrower_Id")
);

CREATE TABLE IF NOT EXISTS public.loan_data
(
	"Borrower_id" text,
	loan_id text,
	"Date_of_release" timestamp without time zone,
	"Term" bigint,
	"InterestRate" double precision,
	"LoanAmount" bigint,
	"Downpayment" bigint,
	"Payment_frequency" double precision,
	"Maturity_date" text,
	 CONSTRAINT  loan_id_pk
			PRIMARY KEY (loan_id),
	 CONSTRAINT borrower_id_fk
			foreign key ("Borrower_id") 
			references public.borrower("Borrower_Id")
			ON DELETE CASCADE
			ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS public.payment_schedule
(
    loan_id text,
    schedule_id text NOT NULL,
    "Expected_payment_date" timestamp without time zone,
    "Expected_payment_amount" double precision,
	 CONSTRAINT schedule_id_pk
			PRIMARY KEY (schedule_id),
	 CONSTRAINT loan_id_fk 
			foreign key ("loan_id") 
			references public.loan_data("loan_id")
			ON DELETE CASCADE
			ON UPDATE CASCADE
	
);

CREATE TABLE IF NOT EXISTS public.repayment_data
(
    loan_id_fk text,
    payment_id_pk text NOT NULL,
    "Amount_paid" timestamp without time zone,
    "Date_paid" double precision,
	 CONSTRAINT payment_id_pk
			PRIMARY KEY (payment_id_pk),
	 CONSTRAINT loan_id_fk 
			foreign key ("loan_id_fk") 
			references public.loan_data("loan_id")
			ON DELETE CASCADE
			ON UPDATE CASCADE
);
